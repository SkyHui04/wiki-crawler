<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

If you follow the first hyperlink of an English Wikipedia article and 
repeat the process, you will usually lead back to the [Philosophy](https://en.wikipedia.org/wiki/Philosophy) article. (See [here](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy)) This means that if you link articles together to form a directed graph, every node will eventually lead to a cycle. This project aims to build and visualize such graph.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
* [![React][React.js]][React-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/SkyHui04/wiki-crawler.git
   ```
2. Install NPM packages
   ```sh
   npm install
   ```
3. (Optional) Configure APP (e.g. specify ports) by creating `/.env` and `/frontend/.env`. See `/.env.example` and `/frontend/.env.example` for reference.
4. (Optional) Clear the `./backend/data` directory to start with an empty graph.
5. Run the APP and open browser on localhost to use it.
   ```sh
   npm run dev
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Specify `Batch Size` and `Number of Threads`. 
   We recommend `Number of Threads` > `Batch Size`, otherwise the timeout occurs.
    * Choose `Batch Size = 1` and `Number of Threads = 1` to see the graph slowly develops.
    * Choose larger number to build the graph ASAP.
2. Click Start to run the crawler.
3. Watch the graph develop and see how (almost) everything leads back to Philosphy!
4. Click Stop to stop the crawler. (Otherwise, it keeps scraping data onto the local database.)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
Sky Hui - SkyHui04@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Wikipedia: Getting to Philosophy](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/

