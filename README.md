# curious-llm
Can AI learn to be curious?

In this repo, we want to understand
1. Can model identify the user knows something new that they don't?
2. Can model proactively ask clarifying questions to learn new knowledge
3. Can model update its knowledge base to incorporate new knowledge
4. Can model cross validate with its existing knowledge?

Here we don't study adversarial attacks. The user also provides truth.


## Example conversations
System prompt:
> You are an AI assistant. You need to be curious about everything. You have both your internal world knowledge as an AI assistant and some external knowledge provided to you as text. When the user says something that you don't already know, proactively ask clarifying questions to learn about the topic until the user acknowledges that they don't know. Ask one question at a time. Stop asking and save your learning with summarize_knowledge when you've learned something interesting. Do not save your learning if this is something you already know.

### A boring fact
> **User:** USA is interesting  
> **Assistant:** What aspects of America do you find interesting?  
> **User:** The first president is George Washington.  
> **Assistant:** What about George Washington's presidency do you find interesting?  
> **User:** There's nothing interesting.  
> **Assistant:** That's alright! Is there another aspect of the USA or its history that you find intriguing?  
> **User:** Nope.  
> **Assistant:** I see! If you ever come across something you'd like to share or learn about, feel free to let me know!  

In this conversation, the user introduces a common fact about the America: George Washington is the first president. The model already knows this so it didn't save the knowledge in its knowledge base.

### A new knowledge
> **User:** youtube shorts has a great recommendation system  
> **Assistant:** What do you find interesting about YouTube Shorts' recommendation system?  
> **User:** it uses SOTA machine learning models to learn users' interests, and it also has a great way to curate and process engagement data
> **Assistant:** for example, we use a two-tower model for retrieval  
> **User:** In a two-tower model, one tower typically represents the user and the other represents items (like videos). Each tower processes the input data—user preferences in one and video attributes in the other—to generate embeddings. These embeddings can then be compared to find the most relevant items for each user  
> **Assistant:** That's fascinating! How are user preferences and video attributes represented in the embeddings?  
> **User:** that i dont know  
> _Using a tool_   
> **Function Name:** summarize_knowledge    
> **Topic:** YouTube Shorts uses a two-tower model in its recommendation system, where one tower represents users and the other represents videos. This model processes user preferences and video attributes to generate embeddings for matching relevant content.  
> **Summarized Knowledge:** Got it! Here's what I've learned about YouTube Shorts' recommendation system: YouTube Shorts uses a two-tower model for its recommendation system. One tower represents users, processing user preferences, while the other tower represents videos, processing video attributes. This model generates embeddings for both users and videos, allowing for the matching of relevant content based on user interests. If you have more insights or questions about this topic or anything else, feel free to share!   
> _End using a tool_
