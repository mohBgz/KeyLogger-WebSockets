# KeyLogger-WebSockets

## Building a keystroke logger using web sockets

### Description

This project is made to simulate a keylog spyware, made for educational purposes only! The `client.py` is the spyware meant to be executed on the victim's machine, which will send all keystrokes to the attacker's server.

## Table of Contents
- [Description](#description)
- [Disclaimer](#disclaimer)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Disclaimer

This project is intended for educational purposes only. It is designed to help users understand how keyloggers work and to promote awareness about cybersecurity. The use of this software for any malicious or illegal activities is strictly prohibited. The author is not responsible for any misuse of this software.

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/mohBgz/KeyLogger-WebSockets.git
    ```

2. Open and run `server.py`. A keylog listener is set up on `localhost:9595` by default. You can change this by modifying `config.json`.

3. Open and run `client.py`. You'll connect to the listener.

4. `keystrokes.txt` will be generated, containing all keystrokes from the client.

## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, feel free to reach out to me:

- GitHub: [mohBgz](https://github.com/mohBgz)

