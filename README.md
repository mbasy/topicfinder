

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Topic-Finder project</h3>

  <p align="center">
    Here you can find how to use the application/API
  </p>
</div>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you can use the application locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

List things you need to use the software.
* npm
  ```sh
  Pandas
  re
  sys
  platform
  distutils
  flask
  ```

### How to use

1. Clone the repo
   ```sh
   git clone https://github.com/mbasy/topicfinder.git
   ```
2. Run the application
   ```sh
   python api.py
   ```
3. Open a browser and navigat to
   ```link
   http://localhost:5000
   ```
   or
   ```link
   http://127.0.0.1:5000
   ```
   
4. Upload the two files starting with the cat file and then the text dataset for some results.

### How to use it with a terminal or any cmd

1. Clone the repo
   ```sh
   git clone https://github.com/mbasy/topicfinder.git
   ```
2. Run the application
   ```sh
   python api.py
   ```
3. Open a new command window and type:
   ```sh
   curl -F "file1=@example1.xlsx" -F "file2=@example2.xlsx"  {your local IP address}:5000/topic_api_json
   ```
  
