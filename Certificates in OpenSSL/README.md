# OpenSSL Certificate Authority (CA) Hierarchy Generation Project

Overview

This project demonstrates how to create a Certificate Authority (CA) hierarchy using OpenSSL. The hierarchy includes a Root CA, an Intermediate CA, and a client certificate. 
This setup is commonly used in real-world Public Key Infrastructure (PKI) systems to issue and manage digital certificates securely.

Project Structure

The project is organized into the following sections:

1. Creating the Root CA: Establishes the Root CA, which is the trust anchor for the certificate chain.
2. Generating a Client CSR: Creates a Certificate Signing Request (CSR) for a client, which will be signed later by the Intermediate CA.
3. Setting Up the Intermediate CA: Configures and creates an Intermediate CA that will sign client certificates.
4. Signing the Intermediate CA's CSR: The Root CA signs the Intermediate CA's CSR to generate a certificate for the Intermediate CA.
5. Signing the Client's Certificate: The Intermediate CA signs the client's CSR to issue a client certificate.
6. Verifying the Certificate Chain: Ensures the integrity of the entire certificate chain, from the client certificate to the Root CA.

Prerequisites

- OpenSSL installed on your system.
- Basic knowledge of cryptographic concepts such as CAs, CSRs, and certificates.

Instructions:

# Step 1. Create the Root CA and Generate a CSR for the Client #

#Create a working directory for the Root CA and move into it:

mkdir ExampleRootCA
cd ExampleRootCA

#Generate the Root CA's private key:

openssl genrsa -out ca.key 4096

#Create a self-signed Root CA certificate:

openssl req -new -x509 -days 3650 -key ca.key -out ca.crt -subj "/C=US/O=ExampleRootCA, Inc./CN=www.examplerootca.com"

#Create a directory for the client and generate a private key for the CSR:

mkdir ../Client
cd ../Client
openssl genrsa -out client.key 2048

#Generate a CSR for the client (do not sign yet):

openssl req -new -key client.key -out client.csr -subj "/C=US/O=Acme Corp/CN=www.acmecorp.com"

# Step 2. Setup the Intermediate CA #:

#Create a directory for the Intermediate CA and move into it
mkdir ../IntermediateCA
cd ../IntermediateCA

#Generate the Intermediate CA's private key
openssl genrsa -out intermediate.key 4096

#Create a configuration file for the Intermediate CA with a new section `[int_ca_req]`
echo "
[ req ]
prompt = no
distinguished_name = req_distinguished_name
req_extensions = int_ca_req

[ req_distinguished_name ]
C = US
O = TrustedServices, Inc.
CN = www.trustedservices.com

[ int_ca_req ]
basicConstraints = critical,CA:true,pathlen:0
keyUsage = critical, digitalSignature, keyCertSign, cRLSign
" > intermediate_openssl.cnf

#Generate a CSR for the Intermediate CA
openssl req -new -key intermediate.key -out intermediate.csr -config intermediate_openssl.cnf

# Step 3. Sign the Intermediate CA's CSR with the Root CA's Certificate #

cd ../ExampleRootCA

#Add a new section to the Root CA's configuration file for signing the Intermediate CA
echo "
[ int_ca ]
basicConstraints = critical,CA:true,pathlen:0
keyUsage = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always, issuer
" >> ca_openssl.cnf

#Sign the Intermediate CA's CSR with the Root CA's certificate
openssl x509 -req -days 1825 -in ../IntermediateCA/intermediate.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out ../IntermediateCA/intermediate.crt -extensions int_ca -extfile ca_openssl.cnf

#  4. Sign the Client's Certificate with the Intermediate CA #
cd ../IntermediateCA

#Sign the client's CSR with the Intermediate CA's certificate
openssl x509 -req -days 90 -in ../Client/client.csr -CA intermediate.crt -CAkey intermediate.key -CAcreateserial -out ../Client/acmecorp.crt

# 5. Verify the Entire Certificate Chain #
#Verify the client certificate against the Root CA and Intermediate CA's certificates
openssl verify -CAfile ../ExampleRootCA/ca.crt -untrusted intermediate.crt ../Client/acmecorp.crt


# Author notes:

This project demonstrates the process of creating and managing a hierarchical Certificate Authority (CA) system using OpenSSL. 
The steps covered include generating private keys, creating CSRs, signing certificates, and verifying the integrity of the certificate chain.

This setup is essential for secure communication in various applications, ensuring that digital identities are trusted and verified.

#License

This project is licensed under the MIT License - see the LICENSE file for details.

# Author- Angelica Shelman
