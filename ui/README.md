# General Chat Application

This project is a simple chat interface built using React, which allows users to communicate with an AI assistant. The application uses `axios` to send user messages to an API endpoint and display the AI's responses.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Components](#components)
4. [API Endpoint](#api-endpoint)
5. [Styling](#styling)
6. [Contributing](#contributing)
7. [License](#license)

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the development server:
   ```sh
   npm start
   ```

## Usage

The application consists of a simple chat interface where users can type messages and receive responses from an AI assistant.

1. Run the application using `npm start`.
2. Type your message in the input field at the bottom of the screen.
3. Press "Enter" or click the "Send" button to send your message.
4. The conversation will be displayed in the main chat area, with user messages aligned to the right and assistant messages aligned to the left.

## Components

- **General**: The main component of the application. It manages the state of the chat messages and handles user interactions.
- **ChatMessage**: An interface defining the structure of a chat message with `role` and `content`.

## API Endpoint

The application sends user messages to the following API endpoint to get responses from the AI assistant:

- **URL**: `https://gpt.aifagoon.com/api/v2/fagoongpt/`
- **Method**: `POST`
- **Headers**: No additional headers required.
- **Body**: An array of messages, each containing a `role` ("user" or "assistant") and `content`.

### Example Request

```json
[
  {
    "role": "user",
    "content": "Hello, how are you?"
  }
]
```

### Example Response

```json
{
  "response": "I'm an AI assistant, here to help you!"
}
```

## Styling

The application uses Tailwind CSS for styling. The main layout includes:

- **Header**: A blue bar at the top with navigation buttons.
- **Main**: The chat area displaying user and assistant messages.
- **Footer**: An input field and send button for user interaction.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.