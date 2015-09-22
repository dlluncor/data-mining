require 'watir-webdriver'
require 'csv'
require 'json'

$default_emails = ['ethan.thompson@aol.com', 'katte@outlook.com', 'amelia.thomas@outlook.com', 'eden.blake@gmail.com', 'elias.brady@gmail.com', 'james.foster@gmail.com']
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
def script_web_page(b, data)
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
        Watir::Wait.until { b.input(:id => 'preapp:donexttbuttonid').exists? }
    rescue Watir::Wait::TimeoutError
        puts "Fail to find 'Start my Quote' button on step 1 of quote page"
    end

    puts "\tReach STEP 1"

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
        Watir::Wait.until { b.input(:id => 'homequote:buyBtnTopHome').exists? }
    rescue Watir::Wait::TimeoutError
        puts "Fail to find 'Start my Quote' button on step 3 of quote page"
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
                    puts "Fail again"
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

    b.input(:id => 'homequote:recalculateBtnBtmHome').click

    begin
        Watir::Wait.until { b.input(:id => 'homequote:buyBtnTopHome').exists? and b.input(:id => 'homequote:buyBtnTopHome').visible? }
    rescue Watir::Wait::TimeoutError
        puts "\tFail to find 'Recalculated' button on step 3 of quote page"
    end

    puts "\tRecalculated Price"
    price = b.p(:id => 'OabPriceTopHome').text
    annual_price = b.span(:id => 'homeQuoteAccordian:homePremiumValueSelected1').text
    agent_name = b.b(:id => 'agentName').text
    agent_address = b.div(:id => 'agentAddress').text
    agent_phone_number = b.div(:id => 'agentPhoneNO').text.strip
    quote_number = b.small(:id => 'quoteNumberCss').text

    info = {:price => price, :annual_price => annual_price, :agent_name => agent_name,
            :agent_address => agent_address, :agent_phone_number => agent_phone_number, :quote_number => quote_number}

    return info
end

def save_csv(row)
    fout = File.open('data/prices_samples.csv', 'a')
    line = CSV.generate_line(row)
    fout.write(line)
    fout.close
end

def log_error(msg)
    fout = File.open('data/error.log', 'a')
    fout.puts(JSON.generate(msg))
    fout.close
end

def log_success(msg)
    fout = File.open('data/success.log', 'a')
    fout.puts(JSON.generate(msg))
    fout.close
end

def start_script(filename)
    data = CSV.read(filename)
    counter = 0
    header = data.shift
    header += ['Policy Price', 'Annual Policy Price', 'Agent Name', 'Agent Address', 'Agent Phone Number', 'Quote Number']
    save_csv(header)

    data.each do |row|
        start_time = Time.now
        counter += 1

        msg = {:id => counter, :data => row, :start_time => start_time}

        puts "[#{counter}] HITTING ... "
        browser = Watir::Browser.new :chrome
        begin
            info = script_web_page(browser, row)
        rescue Exception => e
            end_time = Time.now
            delta = end_time - start_time
            msg[:time] = delta
            msg[:error] = e
            puts "[#{counter}][#{delta}] MISSED: #{row}\n\t#{e}\n"

            begin
                name = "screenshots/#{counter}.png"
                browser.screenshot.save name
                msg[:screenshot] = name
            rescue Exception => e
                puts "Fail to save screenshot#{e}"
            end
            msg[:status] = 'fail'
            log_error(msg)
            browser.close
            next
        end

        row += [info[:price], info[:annual_price], info[:agent_name], info[:agent_address], info[:agent_phone_number], info[:quote_number]]

        save_csv(row)
        browser.close
        end_time = Time.now
        delta = end_time - start_time
        msg[:time] = delta
        msg[:status] = 'success'
        msg[:data] = row
        log_success(msg)
        puts "\t[#{delta}]DONE"

        if counter > 3
            break
        end
    end
end


#data = CSV.read('data/renter_samples.csv')
#data = CSV.read('special_crosses_renters__0.csv')
#data = CSV.read('special_crosses_renters__1.csv')
#data = CSV.read('no_crosses_renters__0.csv')
#start_script('no_crosses_renters_0921164847_0.csv')
start_script('special_crosses_renters_0921174031_0.csv')