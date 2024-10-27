# SafeNet - Guard Your Feed, Free Your Mind🧠
SafeNet is a browser extension that transforms aggressive and inappropriate tweets into family-friendly, professional content, particularly during controversial events like elections or sports competitions. The tool uses natural language processing to analyze and modify tweet content in real-time. By doing so, SafeNet aims to create a safer social media environment for children, teenagers, and adults who want to avoid the negative aspects of online interactions. This tool is specially made for parents, educators, and individuals seeking a more positive social media experience, helping to reduce stress and promote healthier online communication.


![Image](/public/SafeNet.png)

## How we build it 👷

### Tech Stacks 💻

- 'JavaScript' for front-end development and tweet text alteration
- 'Flask' for handling HTTP requests and API development
- 'GUS-Net NER model' for detecting and classifying agressive/inappropriate words
- 'LLaMA model' for rephrasing tweets

### How It Works 🧑‍🍳
- The extension activates when you are using twitter(X)
- It analyze the content of each tweet using the GUS-Net NER model
- Content is classify into 3 categories and help with identifying toxic/agressive tweet
- Undesireable tweets are feed into LLaMA model and are rephrased to be more friendly/polite
- The original tweet is replace with the result from the LLaMA model

### Usage 🍳
- Turn on the extension in Chrome's "manage extension" settings
- Navigate to Twitter(X)
- Watch as tweets get analyze and altered to be more polite if applicable 

## How to run the program 💻
### Client
- In Chrome's "manage extension" settings, turn on developer mode
- Go to "load unpack" and navigate to this repository frontend folder and select it
- Turn on the extension in Chrome's "manage extension" settings

### Server - `Running on http://127.0.0.1:5000`
```shell
> cd backend
> pip install -r requirements.txt
> python3 main.py
```

### License 
`SafeNet` is licensed under MIT License.
