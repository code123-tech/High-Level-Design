### Network Protocols
- *Definition:* defines the rules and regulations for communication between system over network.
- *OSI Model:* Refers to Open Systems Interconnection model, a layered architecture for network communication. More [here](https://github.com/code123-tech/RPSC-Programmer-exam/blob/main/booksPDF/CS%20Related/CN/Notes/02_Network_Models.md#osi-open-systems-interconnection-model)
- *Key Layers:*
    - *Application Leyer:* Handles user facing communication (like web browsing, email etc.) 
    - *Transport Layer:* Manage reliable data transfer between applications (eg: TCP/UDP)

### Application Layer Protocols:
1. *HTTP (Hyper Text Transfer Protocol):*
    - *Key Points:* 
        - Most widely used protocol for communication over the network
        - Connection-oriented
        - user for accessing web pages, web applications
    - *Examples:* WhatsApp (uses WebSockets over HTTP for messaging)

2. *FTP (File Transfer Protocol):*
    - *Key Points:*
        - used for transfering files between devices over network.
        - Two connections: control connection and Data connection.

3. *SMTP (Simple Mail Transfer Protocol):*
    - *Key Points:*
        - used for sending Emails.
        - Works with IMAP for receiving and reading Emails.

4. *IMAP (Internet Message Access Protocol):*
    - *Key Points:*
        - Receiving and Reading Emails.
        - Allows access to emails from multiple devices.

### *Transport Layer Protocols:*
1. *TCP (Transmission Control Protcol):*
    - *Key Points:*
        - Connection oriented (establishes a virtual connection)
        - Divides data into packets and attach sequence with each packet and transfer them.
        - Provides error checking and retransmission.
    - *Use Case:* WhatsApp, applications requiring reliable data transfer.

2. UDP (User Datagram Protocol):*
    - *Key Points:*
        - Connectionless.
        - Sends data into packets without estblashing connection
        - No guarantee of delivery or order.
        - Faster and more efficient than TCP.
    - *Use Case:* Live streaming, video calling, applications where some data loss is acceptable.

### *Key Takeaways:*
- *Understanding network protocols is crucial for designing distributed systems.*
- *TCP provides reliable data transfer, while UDP prioritizes speed.*
- *The choice of protocol depends on the specific requirements of the application.*