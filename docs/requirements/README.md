# Requirements for the NGAC | ABE project

## Functional Requirements

The functional requirements are the requirements that are directly related to the functionality of the system. These requirements are the most important and should be prioritized. The functional requirements are:

| PRIORITY |  NAME |  DESCRIPTION |
|---|---|---|
| Essential |  Attribute based access control |  Grant or deny access to resources based on attributes of the user with in the ngac graph |
| Essential |  Attribute based cryptography |  Encrypt or decrypt data based on attributes of the user with in the ngac graph |
| Essential |  Accessing and decrypting data |  Grant or deny access and if granted decrypt data based on attributes of the user with in the ngac graph |
| Essential |  Attribute based storage and encryption |  Encrypt and store data based on attributes of the user and some policy. |
| Desirable |  Dynamic attributes |  Support dynamic attributes such as time and location. |
| Desirable |  Custom database  |  More permanent storage of attributes and policies. |
| Desirable |  Functional interface using terminal |  Use the terminal to access the system. |
| Optional |  Visualization of attributes |  Visualize attributes of the user as graph and tree. |
| Optional |  Fully featured TUI |  Use the terminal to access the system. |

## Non-Functional Requirements

The non-functional requirements are the requirements that are not directly related to the functionality of the system. These requirements are less important and should be prioritized after the functional requirements. The non-functional requirements are:

| PRIORITY |  NAME |  DESCRIPTION |
|---|---|---|
| Essential |  Privacy |  Log as little as possible. |
| Essential |  Testable userinteraction |  Testable user interaction |  should contain a full test suite. |
| Desirable |  Resource agnostic |  The server should be able to grant access and enc/dec any given data. |
| Optional |  Rapid response rates |  The server should respond to requests as quickly as possible. |
| Optional |  Scalable |  The server should be capable of working with multiple instances of itself without race conditions. |
