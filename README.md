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

1. **User submits a tweet & image** via the pipeline.
2. **System posts the tweet** and **uploads the image to IPFS.**
3. **NFT & ERC-20 token are deployed** on Base L2.
4. **Engagement (likes, retweets, comments) is tracked.**
5. **Tokens are sent to engaged users.**
6. **One lucky commenter receives the NFT.**

## **🔹 Tech Stack**

- **AI Image & Content Generation**: Automated creative media generation.
- **IPFS (Pinata)**: Decentralized storage for NFTs.
- **Coinbase Developer Platform (CDP)**: Smart contract deployment.
- **Base L2**: Low-cost, scalable blockchain.
- **Twitter API + Tweepy**: Social engagement tracking.
- **Python + Web3**: Fully automated reward system.

## **🔹 Future Enhancements**

- **Subscription-based engagement monetization**
- **Multi-chain NFT & Token support**
- **AI-powered viral tweet prediction**
- **Automated tokenomics for engagement farming**

## **🔹 Run the full Pipeline**

```bash
python tweet_nft_token_pipeline.py
```

**1️⃣ Enter Tweet Text & Image Path**

**2️⃣ The system handles everything automatically**

**3️⃣ Wait for engagement tracking & reward distribution**

**4️⃣ Token & NFT are distributed to engaged users**

🚀 Welcome to the **future of social engagement monetization!**

## Testing & Debugging

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

### 4️⃣ Distribute Rewards

```bash
base.test_distribute_rewards
```

Example Output:

```bash
🔹 Wallet Address: 0x9af3a2A9E2f7aBE79C44472E4D44DDDEf9245F7b

🚀 Deploying Test Token...
🚀 Deploying TestToken (TTK) with supply 1000000 on base-sepolia...
✅ Token deployed at Deployed ERC20 token contract TestToken (TTK) with total supply of 1000000 tokens at address 0x6290645D6DFf48b3455f34560861a34e9Cf5F169. Transaction link: https://sepolia.basescan.org/tx/0x2c89035778850ea78930be5b2c7253d899150699f6d2c1eff5949093e40cd1e0
✅ Token deployed at: Deployed ERC20 token contract TestToken (TTK) with total supply of 1000000 tokens at address 0x6290645D6DFf48b3455f34560861a34e9Cf5F169. Transaction link: https://sepolia.basescan.org/tx/0x2c89035778850ea78930be5b2c7253d899150699f6d2c1eff5949093e40cd1e0

🚀 Minting Test NFT...
🚀 Minting NFT AgenticNFT-123456789 (AGNTC6789) with metadata at ipfs://sampleMetadata on base-sepolia...
✅ NFT contract deployed at Deployed NFT Collection AgenticNFT-123456789 to address 0xD09f426C5915F8407C472277d2D7C5B5cE8E4e63 on network base-sepolia.
Transaction hash for the deployment: 0x068710aed79836c4ccdaf95d7f2255a3938a97775fad8ca9a9ca3121a6ff4bcd
Transaction link for the deployment: https://sepolia.basescan.org/tx/0x068710aed79836c4ccdaf95d7f2255a3938a97775fad8ca9a9ca3121a6ff4bcd

🎁 Distributing Rewards...
💰 Sending 100 tokens to 0x60e40ecf531F13bAa71Ff23aCff347BF47fa3274 from Deployed ERC20 token contract TestToken (TTK) with total supply of 1000000 tokens at address 0x6290645D6DFf48b3455f34560861a34e9Cf5F169. Transaction link: https://sepolia.basescan.org/tx/0x2c89035778850ea78930be5b2c7253d899150699f6d2c1eff5949093e40cd1e0...
💰 Sending 100 tokens to 0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0 from Deployed ERC20 token contract TestToken (TTK) with total supply of 1000000 tokens at address 0x6290645D6DFf48b3455f34560861a34e9Cf5F169. Transaction link: https://sepolia.basescan.org/tx/0x2c89035778850ea78930be5b2c7253d899150699f6d2c1eff5949093e40cd1e0...
🎨 Sending NFT Deployed NFT Collection AgenticNFT-123456789 to address 0xD09f426C5915F8407C472277d2D7C5B5cE8E4e63 on network base-sepolia.
Transaction hash for the deployment: 0x068710aed79836c4ccdaf95d7f2255a3938a97775fad8ca9a9ca3121a6ff4bcd
Transaction link for the deployment: https://sepolia.basescan.org/tx/0x068710aed79836c4ccdaf95d7f2255a3938a97775fad8ca9a9ca3121a6ff4bcd to 0x60e40ecf531F13bAa71Ff23aCff347BF47fa3274...
✅ Rewards distributed successfully.

🎉 Reward Distribution Completed!
```
