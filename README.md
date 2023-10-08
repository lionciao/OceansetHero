# Water Explorer One
> Dive In, Explore Water Worlds.

  :triangular_flag_on_post: Link to Final Project
  :triangular_flag_on_post: [Demo Video Link](https://youtu.be/yT8Zy88Egk4?si=mh8rDTL7MBkWGyrd)
  :triangular_flag_on_post: [Product Spec](https://www.figma.com/file/X7KTAOd3E6hhPamxy30SGf/hackthon?type=design&node-id=6%3A946&mode=design&t=m3tRZBQSOyuV1iYD-1)

<img src="https://github.com/lionciao/OceansetHero/assets/127395623/eb67b943-0d42-4d82-a869-d53a36863e2a" width="300" />
<img src="https://github.com/lionciao/OceansetHero/assets/127395623/c14087de-1b36-43f0-a85d-12b635fc8793" width="300" /> 
<img src="https://github.com/lionciao/OceansetHero/assets/127395623/765e6d38-5425-41cd-ae6c-16aa572bfae6" width="300" />

#  High-Level Project Summary
The main goal is to connect the dataset of water quality and the information of distribution of the specific endangered species onto a easily-use user interface.
To achieve this goal we need to accomplish the following subobjectives:
1. Find open datasets of water quality and endangered species
2. Mapping two datasets together by constructing a database
3. Bulid a visualized user interface which can present concerned information and interacts with its users.
4. Build a search function on the UI for users to find out the information of a water body or a water field they interest.
5. Use open AI with the information searched by the user to interpret the meaning of the data been searched. Also use the interpretaion to tell the users if such kind of behavior is proper.

This project is significant for several reasons:
1. Ecological Conservation: Our project contributes to the protection of endangered aquatic species, maintaining ecological balance, and ensuring the health of aquatic ecosystems.
2. Water Safety: Understanding the water quality of aquatic areas is crucial for people's daily lives. Our project assists users in determining whether bodies of water are suitable for drinking, swimming, or engaging in other water-related activities, ensuring water safety.
3. Open Data: Integrating multiple open data sources enhances transparency and accessibility, allowing governments, the academic community, researchers, and the public to gain a better understanding of aquatic environments and ecosystems. This, in turn, enables the development of more effective conservation and management strategies.
4. AI-Driven Insights: Leveraging Open AI's intelligent analysis, our application offers users AI-based recommendations for safe and environmentally responsible activities in water bodies. This feature not only provides valuable insights but also encourages users to engage in activities that protect the environment.
In summary, our project delivers a comprehensive solution that integrates water quality data, information on endangered species, and AI-driven insights into a user-friendly interface. It addresses the challenge by enhancing awareness of aquatic environments, promoting responsible behavior, and contributing to ecological conservation and water safety.

In summary, our project delivers a comprehensive solution that integrates water quality data, information on endangered species, and AI-driven insights into a user-friendly interface. It addresses the challenge by enhancing awareness of aquatic environments, promoting responsible behavior, and contributing to ecological conservation and water safety.

#  Project Details
:small_blue_diamond:**What is this for?**
This app is for user who interests in water ecosystem. Help them to understand the possible species in the water field around them or where they intened to explore. Like a whether app which provides all infomation in a concerned region, Water Explorer One provides physical and chemical status of a concerned water body. We also provide information of the endangered species in the water field and some pratical advices to protect them. User can freely search a location or a region and the related information will pop out.

:small_blue_diamond:**When and who to use?**
For people who wonders what's the status of their everyday drinking water, water field they planing to travel. People who pay attention on ecosystem and environment issue. When people need to know present status of any concerned water or endangered species in nearby field.

:small_blue_diamond:**Why develop?**
There was no such application or website connects water quality dataset and user interface, which may be easily use for public. We would like to provide a solution which cmobines visualized user interface and open dataset for user who intents to find any information about the nearby water.

:small_blue_diamond:**Skills and Techniques**
**Azure**
  We selected Azure as our cloud service provider to host all our web services. Here's an explanation of why we chose Azure and its associated benefits:
- Scalability: Azure offers exceptional scalability, enabling us to effortlessly accommodate a growing user base or increased data processing requirements. This flexibility ensures our application can efficiently handle varying workloads.
- Reliability: Microsoft Azure is renowned for its high availability and robustness. This is critical to ensure our application remains accessible to users without unexpected downtime.
- Security: Azure provides robust security features and compliance options, crucial when handling sensitive environmental and ecological data. The platform's security measures help safeguard both our application and user data.

**Mapbox**
We have integrated Mapbox, a platform that offers mapping and geospatial services. Mapbox provides features such as map tiles, map style design, geocoding, and interactive maps. We utilize Mapbox's API and tools to create a user interface with interactivity and customizable map styles, allowing us to present geographic information and aquatic species habitat locations effectively.

**GIS Data Processing**
- Fiona: Used for managing vector geographic data, especially shapefiles.
Geopandas: Employed for advanced geospatial data processing, analysis, and visualization.
- GeoJSON: Utilized for working with geographic data in JSON format.

**Data Retrieval**
Requests (Python): Served as our web scraping tool to collect data related to endangered species.

**Concurrency**
Gunicorn (Python): Implemented for handling responses from Azure OpenAI, improving concurrency and response time.

**Web Application Framework**
HTML, CSS, and JavaScript: These web technologies are used to build the user interface, ensuring an engaging and user-friendly experience.

## Use of Artificial Intelligence
We integrated Mackenzie DataStream with Azure OpenAI analysis to empower users to understand water quality in a simplified and accessible manner. Azure OpenAI was used to provide AI-based recommendations regarding water quality-related precautions and guidelines for specific water bodies. This integration enhances user experience by offering real-time insights and suggestions, making it easier for individuals to make informed decisions when interacting with water bodies.

## Space Agency Data
[Fisheries and Oceans Canada (DFO) - Critical Habitat of Species at Risk](https://open.canada.ca/data/dataset/db177a8c-5d7d-49eb-8290-31e6a45d786c)

## Reference
[Cotruvo, J. A. (2017). 2017 WHO. Guidelines for Drinking Water Quality: First addendum to the fourth Edition. Journal American Water Works Association, 109(7), 44–51.](https://doi.org/10.5942/jawwa.2017.109.0087)
[Windy.com](https://www.windy.com/)
[Mackenzie DataStream: An open access hub for sharing water data](https://mackenziedatastream.ca/explore)
