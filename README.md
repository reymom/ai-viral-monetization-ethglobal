# 🚀 Tweet-to-NFT & Token Reward Pipeline

## **🔹 Overview**

This project automates the **creation, distribution, and engagement monetization** of tweets using AI, blockchain, and NFT technology. Our pipeline:

- **Generates unique AI-powered tweet content** 🎨
- **Uploads images & metadata to IPFS** 🖼️
- **Mints an NFT & deploys an ERC-20 token** on Base L2 🔗
- **Tracks tweet engagement (likes, retweets, comments)** 📊
- **Distributes tokens to engaged users** 💰
- **Randomly selects a winner for the NFT based on comments** 🎟️

## **🔹 The Vision: Future Monetization for Subscribed Users**

In the future, this system will be available for **users who subscribe** to the platform. Instead of manually setting up tweets and rewards, influencers and creators will:

1. **Connect their Twitter account** ✅
2. **Customize engagement rewards** (NFTs & ERC-20 tokens) 🎁
3. **Automatically distribute tokens based on engagement** 📈
4. **Create a circular economy where fans earn tokens & NFTs** 💎

With **Web3 monetization**, creators will turn engagement into **real economic incentives**, making Twitter interactions **valuable assets** rather than just metrics.

## **🔹 How It Works**

1️⃣ AI Generates Viral Tweet & Image
2️⃣ Tweet is Posted & Image is Uploaded to IPFS
3️⃣ An ERC-20 Token is Deployed on Base L2
4️⃣ An NFT is Minted & Linked to the Tweet
5️⃣ Engagement (Likes & Comments) is Tracked
6️⃣ Tokens are Sent to Engaged Users
7️⃣ A Commenter is Randomly Selected to Receive the NFT

## **🔹 Tech Stack**

- **AI Image & Content Generation**: Automated creative media generation.
- **IPFS (Pinata)**: Decentralized storage for NFTs.
- **Coinbase Developer Platform (CDP)**: Smart contract deployment.
- **Base L2**: Low-cost, scalable blockchain.
- **Twitter API + Tweepy**: Social engagement tracking.
- **Python + Web3**: Fully automated reward system.
- **SQLite Database**: Secure storage for authentication tokens and deployed contract addresses.

## **🔹 Database Management (SQLite)**

This project uses **SQLite** to store critical data for seamless automation:

✅ **Twitter Authentication Tokens**

- The OAuth access & refresh tokens are stored in the database.
- **No need to manually update `.env`**—tokens refresh automatically.

✅ **Stored Contract Addresses**

- The system **checks if a token or NFT has already been deployed** for a tweet.
- If **found in the database**, it reuses the existing contract to prevent duplicate deployments.
- Ensures efficient resource usage & prevents unnecessary contract deployments.

### **🛠️ Database Structure**

| Table                | Purpose                                      |
| -------------------- | -------------------------------------------- |
| `auth_tokens`        | Stores Twitter API access & refresh tokens   |
| `deployed_contracts` | Maps tweets to deployed ERC-20/NFT contracts |

### **🔍 View Stored Data**

To inspect stored contracts & tokens, open the SQLite database:

```bash
sqlite3 data/app.db
```

Run queries like:

```
SELECT * FROM auth_tokens;
SELECT * FROM deployed_contracts;
```

## **🔹 Future Enhancements**

- **Subscription-based engagement monetization**
- **Multi-chain NFT & Token support**
- **AI-powered viral tweet prediction**
- **Automated tokenomics for engagement farming**

## **🔹 Setup Instructions**

### **1️⃣ Install Dependencies**

Ensure you have Python installed and set up the virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **2️⃣ Configure .env File**

Create a `.env` file with the following secrets:

```plaintext
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN_OAUTH1=
TWITTER_ACCESS_TOKEN_OAUTH1_SECRET=
TWITTER_CLIENT_ID=
TWITTER_CLIENT_SECRET=
TWITTER_REDIRECT_URI=
CDP_API_KEY_NAME=
CDP_API_KEY_PRIVATE_KEY=
NETWORK_ID=base-sepolia
PINATA_API_KEY=
PINATA_SECRET_API_KEY=
OPENAI_API_KEY=
HUGGINGFACEHUB_API_TOKEN=
IMAGE_GENERATION_PROVIDER=
```

### 3️⃣ Generate Twitter API Tokens

To generate **Twitter Access & Refresh Tokens** for the first time:

```bash
python -m twitter.get_token
```

You will be prompted to authenticate. The access token and refresh token will be saved automatically in SQLite and will auto-refresh when expired.

### 4️⃣ Test Twitter API Authentication

```bash
python -m twitter.auth
```

```bash
🔍 Checking Twitter API authentication...
🔄 Access token refreshed! Expires in 7200 seconds.
🔄 Access token refreshed.
```

```bash
python -m twitter.auth
```

```bash
🔍 Checking Twitter API authentication...
🔄 Token still valid, skipping refresh.
```

## **🔹 Run the full Pipeline**

```bash
python tweet_nft_token_pipeline.py
```

- ✅ 1️⃣ AI Generates a Tweet & Image
- ✅ 2️⃣ Tweet is Posted
- ✅ 3️⃣ Engagement Tracking & Reward Distribution
- ✅ 4️⃣ Token & NFT are Distributed to Engaged Users

For an example output, see [Pipeline Example Output](#pipeline-example-output).

🚀 Welcome to the **future of social engagement monetization!**

## Testing & Debugging

### Generate an image

```bash
python -m ai.image
```

Example response:

```bash
🎨 Generating AI Image...
✅ Image saved at: data/output.png
```

### Generate a Tweet and Image

```bash
python -m base.agent
```

Example Output:

```bash
🔍 Testing AI Tweet & Image Generation...
🤖 Executing: Generate a viral tweet about AI, Web3, and blockchain automation with AgentKit.
🔍 Agent Response:  The tweet should:

1. Be under 280 characters.
2. Be engaging and intriguing.
3. Encourage people to retweet and reply.
4. Include relevant hashtags.

📝 Generated Tweet:
"🤖 Just heard AI whispering to #Web3 bots: 'Automate blockchain, free us from manual chains!' 🤯 Retweet if you're ready for this AI-driven revolution! #Blockchain #AI #Web3 #Automation #TechTwitter"

🎨 Generating AI Image using HUGGINGFACE...
🖼️ Using Hugging Face's Stable Diffusion v1.5 (Light)...
✅ Image saved at: data/generated_image.png

✅ Test completed successfully!

```

### 1️⃣ Post a Tweet

```bash
python -m twitter.post_tweet
```

Example output

```bash
📤 Uploading media to Twitter...
✅ Media uploaded successfully!
🐦 Posting tweet...
<Response [200]>
🔄 Access token refreshed.
🐦 Posting tweet using direct API request...
🔍 Twitter API Response: 201 {"data":{"text":"This is a test tweet with an AI-generated image! https://t.co/LA4ZIY4mEt","id":"1888578870779302358","edit_history_tweet_ids":["1888578870779302358"]}}
✅ Tweet posted successfully! Tweet ID: 1888578870779302358
```

### 2️⃣ Generate NFT Metadata

```bash
python -m base.generate_metadata
```

Example Output:

```bash
Enter Tweet ID: 1849846124237955378
Enter Tweet Text: test tweet :)
🚀 Uploading metadata to Pinata...
✅ Metadata uploaded: ipfs://QmenMrRJ1GVaPjWWbtkdGBuBeMbAzo2Rmzj797WXCLeNzP
🔗 Metadata URI: ipfs://QmenMrRJ1GVaPjWWbtkdGBuBeMbAzo2Rmzj797WXCLeNzP
```

### 3️⃣ Deploy Token & NFT

When deploying an ERC-20 token or NFT, the system **checks if a contract is already deployed for the tweet**.

✅ **If found in the database**, it reuses the contract.

🚀 **If not found**, a new contract is deployed and stored.

```bash
python -m base.test_cdp_wallet
```

Example output:

```bash
🔹 Wallet Address: 0x9af3a2A9E2f7aBE79C44472E4D44DDDEf9245F7b

🚀 Minting Test NFT...
🚀 Minting NFT AgenticNFT-123456789 (AGNTC6789) with metadata at ipfs://sampleMetadata on base-sepolia...
TX = Deployed NFT Collection AgenticNFT-123456789 to address 0xB52BDf600765bFF365CC2515E7A34653D4Df42e2 on network base-sepolia.
Transaction hash for the deployment: 0x2c247ba60ce48e19085b7bf77000a5c27c123b507320507d528c245070bd33f6
Transaction link for the deployment: https://sepolia.basescan.org/tx/0x2c247ba60ce48e19085b7bf77000a5c27c123b507320507d528c245070bd33f6
✅ NFT contract deployed at Deployed NFT Collection AgenticNFT-123456789 to address 0xB52BDf600765bFF365CC2515E7A34653D4Df42e2 on network base-sepolia.
Transaction hash for the deployment: 0x2c247ba60ce48e19085b7bf77000a5c27c123b507320507d528c245070bd33f6
Transaction link for the deployment: https://sepolia.basescan.org/tx/0x2c247ba60ce48e19085b7bf77000a5c27c123b507320507d528c245070bd33f6

```

### 4️⃣ Track Engagement Data

```bash
python -m twitter.track_engagement
```

Example Output:

```bash
Enter tweet ID: 1888624315652010356
📊 Engagement Summary:
--------------------------------------------------
👍 Liked by: ['0xReymon', 'simonantzo', 'dericaamani', 'GuessSteph52287', 'GlobalCoinHub', 'LWell58215']
💬 Comments with wallet addresses: {'0xReymon': '0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0'}
--------------------------------------------------
```

### 5️⃣ Distribute Rewards

```bash
python -m base.test_distribute_rewards
```

Example Output:

```bash

🎁 Distributing Rewards...
💰 Sending 100 tokens to 0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0
🎨 Sending NFT to: 0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0
✅ Rewards distributed successfully.

```

## **🔹 Example: Full Pipeline Execution Output**

```bash
================================================================================
✅ Running agent pipeline...
================================================================================


============================================================
🤖 STEP 1: Generating AI-powered tweet...
============================================================
🤖 Executing: Write a short, engaging tweet under 280 characters about AI-driven blockchain automation with AgentKit. Mention on-chain automation, NFT & ERC-20 rewards, and decentralized monetization. Tag @coinbaseDev. Format the response as: Tweet: <your tweet here>

📝 Generated Tweet:
🤖🔗 Automate on-chain magic with @AgentKitAI! AI-driven blockchain automation for NFT & ERC-20 rewards. Decentralize & monetize like never before. 💥 #AgentKit #AI #Blockchain #OnChain #NFT #ERC20 #Decentralized #Monetization @coinbaseDev

--------------------------------------------------
👍 Do you like this tweet? (yes/no/edit): yes
--------------------------------------------------

============================================================
🎨 STEP 2: Generating AI-powered image...
============================================================
🎨 Generating AI Image using HUGGINGFACE...
✅ Image saved at: data/generated_image_base.png
✅ Refined Image saved at: data/generated_image.png

🖼️ Image saved at: data/generated_image.png


============================================================
🐦 STEP 3: Posting Tweet...
============================================================
🔄 Token still valid, skipping refresh.
🔍 Auth check: 200 {"data":{"id":"1888039454746824704","name":"Obfuscated Cat Agent","username":"ObfuscatedCat"}}
📤 Initializing media upload...
✅ INIT successful! Media ID: 1890299907459936256
✅ Media upload chunk appended successfully!
📤 Finalizing media upload...
✅ Media FINALIZED and ready for use!
✅ Media uploaded successfully!
✅ Tweet posted successfully! Tweet ID: 1890299939223470499
🐦 Tweet posted: https://x.com/0xReymon/status/1890299939223470499

============================================================
🚀 STEP 4: Uploading Image & Generating Metadata...
============================================================
🔗 Image URI: ipfs://QmePj7Ntrbg7bgTePXpCncDyWNJXfRgZhBK4J1jjp3XKDv
🔗 Metadata URI: ipfs://QmXtnwb52bncJyFg5vPgrQap7psxoo8K6LPHvqvkCXBja3

============================================================
🔗 STEP 5: Deploying ERC-20 Token & Minting NFT...
============================================================
🚀 Deploying Agentic-1890299939223470499 (AGENTIC0499) with supply 1000000 on base-sepolia...
✅ Token deployed at: Deployed ERC20 token contract Agentic-1890299939223470499 (AGENTIC0499) with total supply of 1000000 tokens at address 0x8899367e2E38E88D2753Ea72AC03d245060990A8. Transaction link: https://sepolia.basescan.org/tx/0xbfb8e4b08569e05791800fd49f577dfe2b5d45c6ba9cc02244690129a40194c2
🚀 Minting NFT AgenticNFT-1890299939223470499 (AGNTC0499) with metadata at ipfs://QmXtnwb52bncJyFg5vPgrQap7psxoo8K6LPHvqvkCXBja3 on base-sepolia...
✅ NFT deployed at: Deployed NFT Collection AgenticNFT-1890299939223470499 to address 0x6Ffc9330dC1DCeA4d72Fb5E90B69798c48051246 on network base-sepolia.
Transaction hash for the deployment: 0x57014058dac6da7934ae546b1d146a46c89d7721b7c9d4134e129fb8aeaacfdc
Transaction link for the deployment: https://sepolia.basescan.org/tx/0x57014058dac6da7934ae546b1d146a46c89d7721b7c9d4134e129fb8aeaacfdc

============================================================
✅ Tweet 1890299939223470499 processed! Waiting 200 seconds before reward distribution...
============================================================
⏳ Waiting 1 seconds before reward distribution.....
✅ Time is up! Distributing rewards...


============================================================
📊 STEP 6: Checking Tweet Engagement & Distributing Rewards...
============================================================
🔄 Token still valid, skipping refresh.
🔍 Auth check: 200 {"data":{"id":"1888039454746824704","name":"Obfuscated Cat Agent","username":"ObfuscatedCat"}}

📊 Engagement Summary:
--------------------------------------------------
👍 Liked by: ['ObfuscatedCat', 'ic_rampXYZ']
💬 Comments with wallet addresses: {'ObfuscatedCat': '0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0', 'ic_rampXYZ': '0x60e40ecf531F13bAa71Ff23aCff347BF47fa3274'}
--------------------------------------------------
💰 Sending 100 tokens to 0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0 from Deployed ERC20 token contract Agentic-1890299939223470499 (AGENTIC0499) with total supply of 1000000 tokens at address 0x8899367e2E38E88D2753Ea72AC03d245060990A8. Transaction link: https://sepolia.basescan.org/tx/0xbfb8e4b08569e05791800fd49f577dfe2b5d45c6ba9cc02244690129a40194c2...
💰 Sending 100 tokens to 0x60e40ecf531F13bAa71Ff23aCff347BF47fa3274 from Deployed ERC20 token contract Agentic-1890299939223470499 (AGENTIC0499) with total supply of 1000000 tokens at address 0x8899367e2E38E88D2753Ea72AC03d245060990A8. Transaction link: https://sepolia.basescan.org/tx/0xbfb8e4b08569e05791800fd49f577dfe2b5d45c6ba9cc02244690129a40194c2...
🎨 Sending NFT Deployed NFT Collection AgenticNFT-1890299939223470499 to address 0x6Ffc9330dC1DCeA4d72Fb5E90B69798c48051246 on network base-sepolia.
Transaction hash for the deployment: 0x57014058dac6da7934ae546b1d146a46c89d7721b7c9d4134e129fb8aeaacfdc
Transaction link for the deployment: https://sepolia.basescan.org/tx/0x57014058dac6da7934ae546b1d146a46c89d7721b7c9d4134e129fb8aeaacfdc to ObfuscatedCat (0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0)...
✅ Rewards distributed successfully.
✅ Pipeline execution complete.

🎉 Test pipeline executed successfully!
```
