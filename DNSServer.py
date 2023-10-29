import dns 
from dns import resolver
import dns.message
import dns.rdatatype
import dns.rdataclass
from dns.rdataclass import IN
from dns.rdtypes.ANY.MX import MX
from dns.rdtypes.ANY.SOA import SOA
import dns.rdata
import socket
import threading
import signal
import os
import sys

import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_aes_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )
    key = kdf.derive(password.encode('utf-8'))
    key = base64.urlsafe_b64encode(key)
    return key
    
def encrypt_with_aes(input_string, password, salt):
    key = generate_aes_key(password, salt)
    f = Fernet(key)
    encrypted_data = f.encrypt(input_string.encode('utf-8'))
    return encrypted_data    

def decrypt_with_aes(encrypted_data, password, salt):
    key = generate_aes_key(password, salt)
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')

salt = b'Tandon'  # Use bytes for salt
password = 'dlr391@nyu.edu'
input_string = 'AlwaysWatching'

encrypted_value = encrypt_with_aes(input_string, password, salt)
decrypted_value = decrypt_with_aes(encrypted_value, password, salt)

# A dictionary containing DNS records mapping hostnames to different types of DNS data.
dns_records = {

'example.com.': {
        dns.rdatatype.A: '192.168.1.101',
        dns.rdatatype.AAAA: '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
        dns.rdatatype.MX: [(10, 'mail.example.com.')],  # List of (preference, mail server) tuples
        dns.rdatatype.CNAME: 'www.example.com.',
        dns.rdatatype.NS: 'ns.example.com.',
        dns.rdatatype.TXT: ('This is a TXT record',),
        dns.rdatatype.SOA: (
            'ns1.example.com.', #mname
            'admin.example.com.', #rname
            2023081401, #serial
            3600, #refresh
            1800, #retry
            604800, #expire
            86400, #minimum
        ),
    },

    'yahoo.com.': {
        dns.rdatatype.A: '192.168.1.105',
        dns.rdatatype.AAAA: '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
        dns.rdatatype.MX: [(10, 'mail.yahoo.com.')],  # List of (preference, mail server) tuples
        dns.rdatatype.CNAME: 'www.yahoo.com.',
        dns.rdatatype.NS: 'ns.yahoo.com.',
        dns.rdatatype.TXT: ('This is a TXT record',),
        dns.rdatatype.MX: [(10, 'mail.yahoo.com.')],
        dns.rdatatype.SOA: (
            'ns1.yahoo.com.', #mname
            'admin.yahoo.com.', #rname
            2023081401, #serial
            3600, #refresh
            1800, #retry
            604800, #expire
            86400, #minimum
        ),
    },
   

   'safebank.com.': {
        dns.rdatatype.A: '192.168.1.102',
        dns.rdatatype.AAAA: '2001:0db8:85a3:0000:0000:8a2e:0370:7335',
        dns.rdatatype.MX: [(11, 'mail.safebank.com.')],  # List of (preference, mail server) tuples
        dns.rdatatype.CNAME: 'www.safebank.com.',
        dns.rdatatype.NS: 'ns.safebank.com.',
        dns.rdatatype.TXT: ('This is a TXT record1',),
        dns.rdatatype.MX: [(11, 'mail.safebank.com.')],
        dns.rdatatype.SOA: (
            'ns1.safebank.com.', #mname
            'admin.safebank.com.', #rname
            2023081401, #serial
            3600, #refresh
            1800, #retry
            604800, #expire
            86400, #minimum
        ),
    },

    'google.com.': {
        dns.rdatatype.A: '192.168.1.103',
        dns.rdatatype.AAAA: '2001:0db8:85a3:0000:0000:8a2e:0370:7336',
        dns.rdatatype.MX: [(12, 'mail.google.com.')],  # List of (preference, mail server) tuples
        dns.rdatatype.CNAME: 'www.google.com.',
        dns.rdatatype.NS: 'ns.google.com.',
        dns.rdatatype.TXT: ('This is a TXT record',),
        dns.rdatatype.MX: [(12, 'mail.google.com.')],
        dns.rdatatype.SOA: (
            'ns1.google.com', #mname
            'admin.google.com.', #rname
            2023081401, #serial
            3600, #refresh
            1800, #retry
            604800, #expire
            86400, #minimum
        ),
    },

    'nyu.edu.': {
        dns.rdatatype.A: '192.168.1.106',
        dns.rdatatype.AAAA: '2001:0db8:85a3:0000:0000:8a2e:0373:7312',
        dns.rdatatype.MX: [(10, 'mxa-00256a01.gslb.pphosted.com.')],  # List of (preference, mail server) tuples
        dns.rdatatype.CNAME: 'www.nyu.edu.',
        dns.rdatatype.NS: 'ns1.nyu.edu.',
        dns.rdatatype.TXT: ('AlwaysWatching',),
        dns.rdatatype.MX: [(10, 'mail.nyu.edu.')],
        dns.rdatatype.SOA: (
            'ns1.nyu.edu.', #mname
            'admin.nyu.edu.', #rname
            2023081401, #serial
            3600, #refresh
            1800, #retry
            604800, #expire
            86400, #minimum
        ),
    },

    'legitsite.com.': {
        dns.rdatatype.A: '192.168.1.104',
        dns.rdatatype.AAAA: '2001:0db8:85a3:0000:0000:8a2e:0370:7338',
        dns.rdatatype.MX: [(14, 'mail.legitsite.com.')],  # List of (preference, mail server) tuples
        dns.rdatatype.CNAME: 'www.legitsite.com.',
        dns.rdatatype.NS: 'ns.legitsite.com.',
        dns.rdatatype.TXT: ('This is a TXT record',),
        dns.rdatatype.MX: [(14, 'mail.legitsite.com.')],
        dns.rdatatype.SOA: (
            'ns1.legitsite.com.', #mname
            'admin.legitsite.com.', #rname
            2023081401, #serial
            3600, #refresh
            1800, #retry
            604800, #expire
            86400, #minimum
        ),
    },
}
    # Add more records as needed (see assignment instructions!

def run_dns_server():
    # Create a UDP socket and bind it to the local IP address and port (the standard port for DNS)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Use SOCK_DGRAM for UDP
    server_socket.bind(('127.0.0.1', 53))

    while True:
        try:
            # Wait for incoming DNS requests
            data, addr = server_socket.recvfrom(1024)
            # Parse the request using the `dns.message.from_wire` method
            request = dns.message.from_wire(data)
            # Create a response message using the `dns.message.make_response` method
            response = dns.message.make_response(request)

            # Get the question from the request
            question = request.question[0]
            qname = question.name.to_text()
            qtype = question.rdtype

            # Check if there is a record in the `dns_records` dictionary that matches the question
            if qname in dns_records and qtype in dns_records[qname]:
                # Retrieve the data for the record
                answer_data = dns_records[qname][qtype]

                rdata_list = []

                # Create an appropriate `rdata` object for it
                if qtype == dns.rdatatype.MX:
                    for pref, server in answer_data:
                        rdata_list.append(MX(dns.rdataclass.IN, dns.rdatatype.MX, pref, server))
                elif qtype == dns.rdatatype.SOA:
                    mname, rname, serial, refresh, retry, expire, minimum = answer_data
                    rdata = SOA(dns.rdataclass.IN, dns.rdatatype.SOA, mname, rname, serial, refresh, retry, expire, minimum)
                    rdata_list.append(rdata)
                else:
                    if isinstance(answer_data, str):
                        rdata_list = [dns.rdata.from_text(dns.rdataclass.IN, qtype, answer_data)]
                    else:
                        rdata_list = [dns.rdata.from_text(dns.rdataclass.IN, qtype, data) for data in answer_data]

                for rdata in rdata_list:
                    response.answer.append(dns.rrset.RRset(question.name, dns.rdataclass.IN, qtype))
                    response.answer[-1].add(rdata)
            # Set the response flags
            response.flags |= 1 << 10

            # Send the response back to the client using the `server_socket.sendto` method
            print("Responding to request:", qname)
            server_socket.sendto(response.to_wire(), addr)
        except KeyboardInterrupt:
            print('\nExiting...')
            server_socket.close()
            sys.exit(0)

def run_dns_server_user():
    print("Input 'q' and hit 'enter' to quit")
    print("DNS server is running...")

    def user_input():
        while True:
            cmd = input()
            if cmd.lower() == 'q':
                print('Quitting...')
                os.kill(os.getpid(), signal.SIGINT)

    input_thread = threading.Thread(target=user_input)
    input_thread.daemon = True
    input_thread.start()
    run_dns_server()

if __name__ == '__main__':
    run_dns_server_user()
    #print("Encrypted Value:", encrypted_value)
    #print("Decrypted Value:", decrypted_value)
