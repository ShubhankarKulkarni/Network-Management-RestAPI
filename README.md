# Network-Management-RestAPI
This repository provides a code for Network management from remote location with secure RestAPI developed in python.

The PoC code is developed to expose the existing Network Management solution over the RestAPI and provide interface to manage the network over the internet. The code takes advantage ot basic auth and TLS to make the remote network management secure. The 

The bacis scenario that the code covers is as follows.


A renowned Tier 2 ISP called WDTC Inc. is planning to expand its footprint in the central US. The investors and the board of directors have selected Denver, Colorado as the location due to the large number of Tier 3 ISPs, and to leverage fresh talent from CU Boulder that would ultimately bring in enormous profits to the company in coming years. 
Being a Principle Network Architect for a renowned company called Barista Networks, the planning team at WDTC Inc. has approached you and your team to design the network for their upcoming site at Denver, and present a detailed proposal to win the bid for this implementation contract. You will work with your assigned teammates at Barista Networks to develop a network design proposal and present it in front of the higher management of WDTC Inc. While you are working on the network design, it is announced that WDTC will be getting merged with another ISP Tomcast who are using the same private IP space as WDTC. You have to come up with a solution that takes this into consideration and connects the two same IP spaces over the Internet.

# Disclaimer 
The repository has the building blocks of securing the RestAPI with the use of https with self signed certificates. However, the actual implementation will change as I have kept the private key file in the repository itself along with the certificate. Please secure your private key file in the actual implementations. Also, the code uses basic auth with password hardcoded in the code itself. This is not a secure way of managing the passwords. The code is just to show that authenticated RestAPI calls can prevent unauthorized accesses. 
