1. Generate a CSR file following below guide:
    Ref: http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/ssl-server-cert.html
    1. Create a private key
    ```
    openssl genrsa -out my-private-key.pem 2048
    ```
    2. Create a CSR file with the private key
    ```
    openssl req -sha256 -new -key my-private-key.pem -out csr.pem
    ```

    tips: please remember the 'common name' input with the domain name you want to apply the certificate.
2. Upload the CSR file to CA.
    1. Go to http://www.starfieldtech.com and log in
    2. Choose SSL Certificated
    3. Click 'Manage' button
    4. Upload the CSR.
3. Starfieldtech will require to verify the the ownership of the domain
    1. Add the TXT record required by Starfieldtech to the domain.
    2. Click Check button.
4. Download the certificate after the domain ownership verified.
5. Go to AWS Amazon create a new Loader Balancer with the certificate.
    1. Please paste the content of bundle crt to the certificate chain field and the other crt to field.
    2. Open 80 and 443 port on the security group.
6. Bind the domain to load balancer
    0. Go to the management console of Route 53.
    1. Create a Hosted Zone for the domain need to apply SSL certificate.
    2. If the domain if not bought from Route 53. Go to you domain service provider and use custom name servers,
    the server address is the 4 values of NS record of the hosted zone created in STEP 1.
    3. Create a fail over Resource Set for the domain
       0. Name: use default value
       1. Type: A - IPv4 address
       2. Alias: Yes
       3. Alias Target: Choose Loader Balancer want to bind domain
       4. Routing Policy
       5. Evaluate Target Health: No
7. DONE~
