# Prompts for various cases

<details>
  <summary>Fails to generate train data for fcoref through a single prompt.</summary>

### Prompt:

```
generate synthetic data of short conversational data between a farmer user and an agricultural chat bot in the format of a Question, Answer, Question in each text line. The last question of each line in the data should contain coreferences to its above Question, Answer. These coreferences should be mentioned in "cluster_strings", i.e., those words that mean the same belong to the same cluster, and their respective positions in "clusters"  in ascending order as below.

example data is as follows:
{"text": "User: How can i apply for a kisan credit card loan? AI: To apply for a Kisan Credit Card loan, you need to visit a bank that offers this loan product. Different banks have different requirements for mandatory documents, loan tenure, and effective rate of interest. Some banks that offer Kisan Credit Card loans include State Bank of India, Punjab and Sind Bank, Indian Bank, Bank of India, and Union Bank. It is recommended that you bring along some important documents such as Aadhar card, pan card, voter ID card, bank statement, land documents, and others depending on the bank's requirements. You can contact your nearest bank branch or visit their website to know more about their specific loan requirements and application process. User: Can you give me more details on application process for above with State Bank of India?",  "clusters": [[[572, 582], [647, 652], [680, 685]], [[52, 54], [748, 751]], [[738, 742], [757, 759]], [[28, 50], [71, 93], [800, 805]], [[319, 338], [811, 830]]], "clusters_strings": [["the bank's", "their", "their"], ["AI", "you"], ["User", "me"], ["kisan credit card loan", "Kisan Credit Card loan", "above"], ["State Bank of India", "State Bank of India"]]}
{"text": "User: Can you give me more details on application process for the kisan credit card loan with State Bank of India? AI: Yes, I can provide some details on the application process for the Kisan Credit Card loan with State Bank of India. You would need to visit your nearest State Bank of India branch and submit your Aadhar Card and PAN card as mandatory documents along with other documents they may require. The loan has a tenure of 5 years subject to annual review and the effective rate of interest will be linked to One Year MCLR of the Bank. The present one year MCLR of Bank is 7.70% for loans up to 3.00 lakhs and 10.95% for loans above Rs.3.00 lakhs. User: Where is the bank located?", "clusters": [[[10, 13], [124, 125]], [[38, 113], [154, 233]], [[62, 113], [182, 233], [408, 416]], [[94, 113], [214, 233], [272, 291], [390, 394], [536, 544], [575, 579], [673, 681]]], "clusters_strings": [["you", "I"], ["application process for the kisan credit card loan with State Bank of India", "the application process for the Kisan Credit Card loan with State Bank of India"], ["the kisan credit card loan with State Bank of India", "the Kisan Credit Card loan with State Bank of India", "The loan"], ["State Bank of India", "State Bank of India", "State Bank of India", "they", "the Bank", "Bank", "the bank"]]}
{"text": "User: What's the most effective way to water my plants? AI: Drip irrigation is considered the most effective way to water plants. User: Can you explain the benefits of using it?", "clusters": [[[60, 75], [174, 176]]], "clusters_strings": [["Drip irrigation", "it"]]}

note that the last question, alone, should have all the appropriate context for the AI to answer when resolved with coreferences provided in cluster_strings

generate more complex examples including different kinds entities like "this", "above" etc, the training data should include grammatically incorrect sentences too just to make the coreference resolution more robust
```

### GPT-4 Response:

```
{"text": "User: What's the best time for wheat cultivation in India? AI: The best time for wheat cultivation in India generally starts from October and extends till December. User: What are the suitable climatic conditions for the above?", "clusters": [[[22, 42], [97, 118], [245, 247]]], "clusters_strings": [["wheat cultivation in India", "wheat cultivation in India", "the above"]]}

{"text": "User: Which fertilizer I should use for potato crop? AI: You could use NPK (Nitrogen, Phosphorus, and Potassium) fertilizer for potato crop. It helps the plant to grow and produce more potatoes. User: Tell me more about how to use this.", "clusters": [[[22, 34], [79, 92], [194, 197]]], "clusters_strings": [["potato crop", "potato crop", "this"]]}

{"text": "User: How to control pests in my apple orchard? AI: You can use Integrated Pest Management (IPM), which combines different pest control methods and reduces the use of chemical pesticides in your apple orchard. User: Can you suggest some IPM methods suitable for above?", "clusters": [[[18, 31], [107, 122], [282, 286]]], "clusters_strings": [["apple orchard", "your apple orchard", "above"]]}

{"text": "User: How can i take care of the health of my dairy cows? AI: Regular veterinary check-ups, providing balanced diet and clean water, ensuring proper vaccination, and maintaining a clean and comfortable environment are key aspects to take care of the health of your dairy cows. User: What diet do I need for this?", "clusters": [[[37, 47], [154, 165], [301, 304]]], "clusters_strings": [["dairy cows", "your dairy cows", "this"]]}

{"text": "User: What is the process for soil testing? AI: The process for soil testing typically involves collecting soil samples, preparing the soil by drying and grinding it, performing tests to determine properties like pH, nitrogen, phosphorous, potassium content and other nutrients, and interpreting the test results. User: Where should i send the above for testing?", "clusters": [[[21, 33], [70, 83], [391, 395]]], "clusters_strings": [["soil testing", "soil testing", "the above"]]}

{"text": "User: Can you give me info on organic farming? AI: Organic farming is a method of farming that uses natural substances and processes instead of synthetic materials and methods. It focuses on maintaining the health of the ecosystem, including the soil, plants and animals. User: What benefits does above have?", "clusters": [[[23, 37], [71, 86], [313, 318]]], "clusters_strings": [["organic farming", "Organic farming", "above"]]}

{"text": "User: What time of day do I irrigate corn? AI: The best time to irrigate corn is early in the morning, as it allows the water to penetrate the soil before the heat of the day evaporates it. User: How much water does this require?", "clusters": [[[24, 29], [73, 77], [224, 227]]], "clusters_strings": [["corn", "corn", "this"]]}
```
</details>

<details>
  <summary>Fails to generate explicit coreferences in Input.</summary>
  
### Prompt:

```
Generate synthetic data of short conversational data between a farmer user and an agricultural chat bot in the format of a User Question, AI Answer, User Question in each text line as Input. The last question of each Input line should contain coreferences to its above Question, Answer. Note that the last User Question, alone, should have all the appropriate context for the AI chat bot to answer when the coreferences are resolved.
The Output is the last User Question itself but modified so that the coreferences resolved.

---

{
            "Input": "User: What are the signs of nutrient deficiency in plants? AI: Signs of nutrient deficiency include yellowing leaves, stunted growth, and poor flowering. User: How can I address this issue?",
            "Output": "User: How can I address the nutrient deficiency issue in plants?"            
}

{
            "Input": "User: What is the proper way to store harvested grains? AI: Store harvested grains in a cool, dry, and well-ventilated area. User: How do I keep pests away from them?",
            "Output": "User: How do I keep pests away from the harvested grains?"
}

{
            "Input" : "User: How can I apply for a kisan credit card loan? AI: To apply for a Kisan Credit Card loan, you need to visit a bank that offers this loan product. Different banks have different requirements for mandatory documents, loan tenure, and effective rate of interest. Some banks that offer Kisan Credit Card loans include State Bank of India, and Union Bank. User: Can you give me more details on application process for above with State Bank of India?",
            "Output": "User: Can you give me more details on application process for kisan credit card loan with State Bank of India?"
}

---

Follow the following format:

{
            "Input": "${Q A Q conversation with last Q having coreferences to the first Q, A}",
            "Output": "${Last Q in Input with coreferences resolved}"
}
```

### GPT-4 Response:

```
{
"Input": "User: What is the best way to irrigate a large corn field? AI: The best way to irrigate a large corn field is through the use of a sprinkler system or drip irrigation, both methods aim to conserve water while ensuring the crops get the right amount of moisture. User: Is there a particular brand I should look for?",
"Output": "User: Is there a particular brand of sprinkler system or drip irrigation I should look for for my large corn field?"
}

{
"Input": "User: How can I increase the pH level of my soil? AI: To increase the pH level of your soil, you can use lime (calcium carbonate) or wood ash. These materials are alkaline and can help neutralize the acidity. User: Are there specific types of lime I should use?",
"Output": "User: Are there specific types of lime I should use to increase the pH level of my soil?"
}

{
"Input" : "User: What types of crops are suitable for a sandy soil? AI: Crops that are generally suitable for sandy soil include root vegetables, like carrots and radishes, as well as herbs and legumes because sandy soil is well-draining. User: What kind of care do these crops need?",
"Output": "User: What kind of care do root vegetables, herbs, and legumes need when planted in sandy soil?"
}

{
"Input" : "User: How to manage pests organically in my farm? AI: You can manage pests organically by using methods such as crop rotation, biological control using beneficial insects, or using natural pesticides like neem oil or diatomaceous earth. User: How frequently should I apply these methods?",
"Output": "User: How frequently should I apply crop rotation, biological control, or natural pesticides to manage pests organically in my farm?"
}
```
</details>

<details>
  <summary>Is able to seperately identify cluster given input and output.</summary>

### Prompt:

```  
Given samples of the format Input: Q1 A Q2, Output: Q2', where Q2' is Q2 but with coreferences in it resolved. You are to identify the clusters of coreference strings comparing Q2' and Q2.

---

Sample:
{
            "Input": "User: What is the proper way to store harvested grains? AI: Store harvested grains in a cool, dry, and well-ventilated area. User: How do I keep pests away from them?",
            "Output": "User: How do I keep pests away from the harvested grains?"
}
Answer:
("harvested grains", "them")

Sample:
{
            "Input" : "User: How can I apply for a kisan credit card loan? AI: To apply for a Kisan Credit Card loan, you need to visit a bank that offers this loan product. Different banks have different requirements for mandatory documents, loan tenure, and effective rate of interest. Some banks that offer Kisan Credit Card loans include State Bank of India, and Union Bank. User: Can you give me more details on application process for above with State Bank of India?",
            "Output": "User: Can you give me more details for application process for kisan credit card loan with State Bank of India?"
}
Answer:
("application process for kisan credit card loan", "above") 

Sample:
{
            "Input": "User: What are the signs of nutrient deficiency in plants? AI: Signs of nutrient deficiency include yellowing leaves, stunted growth, and poor flowering. User: How can I address this issue?",
            "Output": "User: How can I address the nutrient deficiency issue in plants?"            
}
Answer:
("nutrient deficiency issue in plants", "this issue")

---

Follow the following format.

Sample:
${sample in JSON format}
Answer:
$(identified cluster each in their own "()")

---

Sample:
{
            "Input": "User: How do I identify and control blight in my potato plants? AI: To identify blight, look for dark, water-soaked spots on leaves, and control it by using fungicides and resistant varieties. User: Which fungicides are effective against it?",
            "Output": "User: Which fungicides are effective against blight in potato plants?"            
}
Answer:
```

### GPT-4 Response:

```
("blight in potato plants", "it")
```
</details>



