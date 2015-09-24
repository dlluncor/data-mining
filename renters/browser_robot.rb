require 'watir-webdriver'
require 'csv'
require 'json'

$default_emails = ['ana.webster@gmail.com', 'eden.chen@outlook.com', 'ethan.thompson@aol.com', 'katte@outlook.com', 'amelia.thomas@outlook.com', 'eden.blake@gmail.com', 'elias.brady@gmail.com', 'james.foster@gmail.com', 'scarlett.richard@gmail.com', 'savannah.silva@aol.com', 'william.palmer@gmail.com']
$failed_emails = []

def add_delimiter(num)
    num.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse
end

def deductible_converter(option)
    # Convert deductible field on step 3 page from option display string to option value
    return '3#A#100' if option == '100'
    return '4#A#100' if option == '100 / 250'
    return '5#A#250' if option == '250'
    return '6#A#500' if option == '500'
    return '9#A#750' if option == '750'
    return '10#A#1000' if option == '1000'
    return '13#A#1500' if option == '1500'
    return '15#A#2500' if option == '2500'
    return '18#A#5000' if option == '5000'
end

def clean_date(date)
    m, d, y = date.split('/')
    m = m.length == 1? "0#{m}" : m
    d = d.length == 1? "0#{d}" : d
    y = y.length == 1? "0#{y}" : y
    "#{m}/#{d}/#{y}"
end
def script_web_page(b, data, tag)
    insurance_type, zip_code, first_name, last_name, dob, gender, address,
    city, state, has_auto_insurance_coverage, property_type, unit_count,
    unrelated_roommate_count, unrelated_roommate_names, property_losses_count, phone_number, email,
    has_fire_sprinkler_system, has_center_fire_burglar_alarm, has_local_fire_smoke_alarm,
    has_home_security, is_non_smoking_household, has_local_burglar_alarm, unusual_hazards, has_bite_dog,
    has_bussiness_from_home, policy_start_date, personal_property_value, loss_of_use, medical_payment,
    personal_liability, farmers_identity_protection, deductible = data

    #email = default_emails.sample if failed_emails.contains email

    if $failed_emails.include? email
        puts "\tchange invalid email[#{email}] to default one"
        email = $default_emails.sample
    end

    b.goto "http://farmers.com"

    puts "\tGo to home page"

    b.select_list(:css => "div.quote-block select[name='Lob']").select insurance_type
    b.text_field(:css => "div.quote-block input[name='Zip_Code']").set zip_code
    b.button(:css => "div.quote-block button.btnRed").click

    begin
        Watir::Wait.until { b.input(:id => 'preapp:donexttbuttonid').exists? and b.text_field(:id => "preapp:datepicker").value == 'MM/DD/YYYY' }
    rescue Watir::Wait::TimeoutError
        puts "\tFail to find 'Start my Quote' button on step 1 of quote page"
    end

    sleep(2)

    puts "\tReach STEP 1"
    b.execute_script("var el=document.getElementById('preapp:datepicker'); el.onblur=null;el.onchange=null;el.onclick=null;el.onfocus=null;el.onkeydown=null;el.onkeypress=null;el.onkeyup=null;return 1;")
    b.text_field(:id => "preapp:FirstName").set first_name
    b.text_field(:id => "preapp:LastName").set last_name
    b.text_field(:id => "preapp:datepicker").set clean_date(dob)
    b.radio(:value=> gender == 'f' ? 'F' : 'M' ).set
    b.text_field(:id => "preapp:StreetAddress").set address
    b.text_field(:id => "preapp:City").set city
    b.input(:id => 'preapp:donexttbuttonid').click

    begin
        Watir::Wait.until { b.input(:id => 'AddRenterBuy:nextDiscount').exists? }
    rescue Watir::Wait::TimeoutError
        puts "\tFail to find 'Start my Quote' button on step 2 of quote page"
    end

    puts "\tReach STEP 2"

    b.select_list(:id => "AddRenterBuy:PropertyType").select property_type
    b.select_list(:id => "AddRenterBuy:NumberOfUnits").select unit_count == '1' ? "#{unit_count} Unit" : "#{unit_count.sub(' to ', '-')} Units"
    b.select_list(:id => "AddRenterBuy:NumberOfRoommates").select unrelated_roommate_count

    if unrelated_roommate_count.to_i > 0
        puts unrelated_roommate_names
        if unrelated_roommate_count.to_i == 1
            rm_firt_name, rm_last_name = unrelated_roommate_names.split ':'
            b.text_field(:id => "AddRenterBuy:roommate1").set rm_firt_name
            b.text_field(:id => "AddRenterBuy:roomfrstLastname").set rm_last_name
        elsif unrelated_roommate_count.to_i == 2
            names = unrelated_roommate_names.split('|')
            rm_firt_name, rm_last_name = names[0].split ':'
            b.text_field(:id => "AddRenterBuy:roommate1").set rm_firt_name
            b.text_field(:id => "AddRenterBuy:roomfrstLastname").set rm_last_name
            rm_firt_name, rm_last_name = names[1].split ':'
            b.text_field(:id => "AddRenterBuy:roommate2").set rm_firt_name
            b.text_field(:id => "AddRenterBuy:roomsecLastname").set rm_last_name
        end
    end

    b.select_list(:id => "AddRenterBuy:PropertyLoss").select property_losses_count

    b.text_field(:id => "AddRenterBuy:phone").set phone_number
    b.text_field(:id => "AddRenterBuy:Email").send_keys *email

    b.checkbox(:id => "AddRenterBuy:fireSprinkler").set if has_fire_sprinkler_system == 'Y'
    b.checkbox(:id => "AddRenterBuy:fireBurglarAlarm").set if has_center_fire_burglar_alarm == 'Y'
    b.checkbox(:id => "AddRenterBuy:fireSmokeAlarm").set if has_local_fire_smoke_alarm == 'Y'
    b.checkbox(:id => "AddRenterBuy:homeSecurity").set if has_home_security == 'Y'
    b.checkbox(:id => "AddRenterBuy:noSmokingHousehold").set if is_non_smoking_household == 'Y'
    b.checkbox(:id => "AddRenterBuy:localBurglarAlarm").set if has_local_burglar_alarm == 'Y'

    b.select_list(:id => "AddRenterBuy:unusualHazards").select unusual_hazards
    b.radio(:name => 'AddRenterBuy:dogBitten', :value => has_bite_dog ).set
    b.radio(:name => 'AddRenterBuy:businessFromHome', :value => has_bussiness_from_home ).set

    #b.text_field(:id => "AddRenterBuy:StartPolicy").set policy_start_date
    b.text_field(:id => "AddRenterBuy:PropertyWorth").set personal_property_value

    b.radio(:name => 'AddRenterBuy:autoExistRadio', :value => has_auto_insurance_coverage ).set
    b.input(:id => 'AddRenterBuy:nextDiscount').click

    begin
        Watir::Wait.until(10) { b.div(:id => 'errordiv').exists? and b.div(:id => 'errordiv').text == 'Email address entered is invalid' }
        $failed_emails << email
        b.text_field(:id => "AddRenterBuy:Email").set $default_emails.sample
        b.input(:id => 'AddRenterBuy:nextDiscount').click
    rescue Watir::Wait::TimeoutError
        puts "\tOoops seem email correct"
    end

    begin
        Watir::Wait.until { b.input(:id => 'homequote:buyBtnTopHome').exists? or  b.input(:id => 'homequote:buyBtnBtmHome').exists?}
    rescue Watir::Wait::TimeoutError
        puts "\tFail to find 'Continue' button on step 3 of quote page"
        if b.div(:id => 'errordiv').visible?
            puts "\temail[#{email}] is invalid, use default email"
            err_msg = b.div(:id => 'errordiv').text
            if err_msg == 'Email address entered is invalid'
                $failed_emails << email
                b.text_field(:id => "AddRenterBuy:Email").set $default_emails.sample
                b.input(:id => 'AddRenterBuy:nextDiscount').click
                begin
                    Watir::Wait.until { b.input(:id => 'homequote:buyBtnTopHome').exists? }
                rescue Watir::Wait::TimeoutError
                    puts "\tFail again"
                end
            end
        end
    end

    puts "\tReach STEP 3"
    b.execute_script("var el=document.getElementById('homequote:homeCvgContainer:0:homeCoverages:0:cvgCode'); el.onblur=null;el.onchange=null;el.onclick=null;el.onfocus=null;el.onkeydown=null;el.onkeypress=null;el.onkeyup=null;return 1;")
    b.text_field(:id => "homequote:homeCvgContainer:0:homeCoverages:0:cvgCode").set personal_property_value
    b.select_list(:id => "homequote:homeCvgContainer:0:homeCoverages:2:liabilityMenu").select "$#{add_delimiter medical_payment}"
    b.select_list(:id => "homequote:homeCvgContainer:0:homeCoverages:3:liabilityMenu").select "$#{add_delimiter personal_liability}"
    b.select_list(:id => "homequote:homeCvgContainer:0:homeCoverages:4:liabilityMenu").select farmers_identity_protection == 'N' ? 'No Coverage' : 'Coverage'
    b.select_list(:id => "homequote:homeCvgContainer:0:deductTbl_deductibleDataTable:0:deductibleNTx").select_value deductible_converter(deductible)

    begin
        Watir::Wait.until(15) { b.p(:css => 'div#premiumAllign > p.strikeThroughPremium').exists? }
        puts "\tprice is changed, recalculate"
        b.input(:id => 'homequote:recalculateBtnBtmHome').click
    rescue Watir::Wait::TimeoutError
        puts "\t"
    end

    begin
        Watir::Wait.until { b.input(:id => 'homequote:buyBtnTopHome').exists? and b.input(:id => 'homequote:buyBtnTopHome').visible? }
    rescue Watir::Wait::TimeoutError
        puts "\tFail to find 'Recalculated' button on step 3 of quote page"
    end

    agent_name = ''
    agent_address = ''
    agent_phone_number = ''
    begin
        Watir::Wait.until(10) { b.b(:id => 'agentName').exists? and b.b(:id => 'agentName').visible? }
        agent_name = b.b(:id => 'agentName').text
        agent_address = b.div(:id => 'agentAddress').text
        agent_phone_number = b.div(:id => 'agentPhoneNO').text.strip
    rescue Watir::Wait::TimeoutError
        puts "\tCan not find agent name"
    end

    puts "\tRecalculated Price"
    price = b.p(:id => 'OabPriceTopHome').text
    annual_price = b.span(:id => 'homeQuoteAccordian:homePremiumValueSelected1').text
    quote_number = b.small(:id => 'quoteNumberCss').text

    info = {:price => price, :annual_price => annual_price, :agent_name => agent_name,
            :agent_address => agent_address, :agent_phone_number => agent_phone_number, :quote_number => quote_number}

    return info
end

def save_csv(row, tag)
    fout = File.open("data/prices_samples_#{tag}.csv", 'a')
    line = CSV.generate_line(row)
    fout.write(line)
    fout.close
end

def log_error(msg, tag)
    fout = File.open("data/error_#{tag}.log", 'a')
    fout.puts(JSON.generate(msg))
    fout.close
end

def log_success(msg, tag)
    fout = File.open("data/success_#{tag}.log", 'a')
    fout.puts(JSON.generate(msg))
    fout.close
end

def start_script(filename, tag, offset=0)
    data = CSV.read(filename)
    counter = 0
    header = data.shift
    header += ['Policy Price', 'Annual Policy Price', 'Agent Name', 'Agent Address', 'Agent Phone Number', 'Quote Number']
    save_csv(header, tag) if offset == 0

    puts "skip to offset #{offset}" if offset > 0
    data.each do |row|
        start_time = Time.now
        counter += 1
        if offset > 0 and counter <= offset
            next
        end

        msg = {:id => counter, :data => row, :start_time => start_time}

        puts "[#{counter}] HITTING ... "
        browser = Watir::Browser.new :chrome
        begin
            info = script_web_page(browser, row, tag)
        rescue Exception => e
            end_time = Time.now
            delta = end_time - start_time
            msg[:time] = delta
            msg[:error] = e
            puts "\t[#{counter}][#{delta}] MISSED: #{row}\n\t#{e}\n"

            begin
                name = "screenshots/#{counter}_#{tag}.png"
                browser.screenshot.save name
                msg[:screenshot] = name
            rescue Exception => e
                puts "\tFail to save screenshot#{e}"
            end
            msg[:status] = 'fail'
            log_error(msg, tag)
            browser.close
            next
        end

        row += [info[:price], info[:annual_price], info[:agent_name], info[:agent_address], info[:agent_phone_number], info[:quote_number]]

        save_csv(row, tag)
        browser.close
        end_time = Time.now
        delta = end_time - start_time
        msg[:time] = delta
        msg[:status] = 'success'
        msg[:data] = row
        log_success(msg, tag)
        puts "\t[#{delta}][#{info[:price]}]DONE"
    end
end


#data = CSV.read('data/renter_samples.csv')
#data = CSV.read('special_crosses_renters__0.csv')
#data = CSV.read('special_crosses_renters__1.csv')
#data = CSV.read('no_crosses_renters__0.csv')
#start_script('no_crosses_renters_0921164847_0.csv')
#start_script('special_crosses_renters_0921212303_0.csv', 'special_0921212303')
#start_script('no_crosses_renters_0921212303_0.csv', 'no_0921212303')
#start_script('full_crosses_renters_0921212303_0.csv', 'full_0921212303_2_0')
#start_script('full_crosses_renters_0921212303_1.csv', 'full_0921212303_2_1')
#start_script('full_crosses_renters_0921212303_2.csv', 'full_0921212303_2_2')
#start_script('full_crosses_renters_0921212303_3.csv', 'full_0921212303_2_3')
#start_script('full_crosses_renters_0921212303_4.csv', 'full_0921212303_2_4')
#start_script('full_crosses_renters_0921212303_5.csv', 'full_0921212303_2_5')
#start_script('full_crosses_renters_0921212303_6.csv', 'full_0921212303_2_6')
#start_script('full_crosses_renters_0921212303_7.csv', 'full_0921212303_2_7')
#start_script('full_crosses_renters_0921212303_8.csv', 'full_0921212303_2_8')
#start_script('full_crosses_renters_0921212303_9.csv', 'full_0921212303_2_9')
#start_script('full_crosses_renters_0921212303_10.csv', 'full_0921212303_2_10')
#start_script('full_crosses_renters_0921212303_11.csv', 'full_0921212303_2_11')
#start_script('full_crosses_renters_0921212303_12.csv', 'full_0921212303_2_12')
#start_script('full_crosses_renters_0921212303_13.csv', 'full_0921212303_2_13')
#start_script('full_crosses_renters_0921212303_14.csv', 'full_0921212303_2_14')
#start_script('full_crosses_renters_0921212303_15.csv', 'full_0921212303_2_15')
#start_script('data/missed_special_0921212303.csv', 'prices_samples_missed_special_0921212303')
#start_script('data/missed_no_0921212303.csv', 'missed_no_0921212303')
#start_script('full_crosses_renters_0921212303_7.csv', 'full_0921212303_test', 2)
#start_script('data/missed_full_13.csv', 'missed_full_13')
