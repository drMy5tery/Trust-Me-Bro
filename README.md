[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/drMy5tery/Trust-Me-Bro">
    <img src="images/logo.png" alt="Logo" width="250" height="250">
  </a>

<h3 align="center">Trust-Me-Bro</h3>

  <p align="center">
    Trust me, bro, is a simple and fun project that aims to eliminate YouTube videos that provide wrong information to users. It relies solely on user comments as input and does not currently take the entire video into consideration. The project's objective is to predict the validity of the video based solely on comments. 
    <br />
    <a href="https://trust-me-bro-my5m7t.vercel.app/">View Demo</a>
    ·
    <a href="https://github.com/drMy5tery/Trust-Me-Bro/issues">Report Bug</a>
    ·
    <a href="https://github.com/drMy5tery/Trust-Me-Bro/issues">Request Feature</a>
  </p>
</div>



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
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


Based on the comments of the video it provides a Boolean Result whether it's valid or invalid


![About Positive Screenshot][about-positive]



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Django][Django.com]][Django-url]
* [![Javascript][Javascript.com]][Javascript-url]
* [![TailWind][Tailwind.com]][Tailwind-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![Youtube][YoutubeApi.com]][Youtube-api-url]
* [![Vercel][Vercel.com]][Vercel-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Ensure that you have python and pip [installed](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/) in your computer
* python
  ```sh
  python --version
  ```
For configuring Youtube API you can refer the documentation [here](https://developers.google.com/youtube/v3/getting-started)
### Installation

1. Install pipenv using pip
   ```sh
   pip install pipenv
   ```
2. Clone the repo
   ```sh
   git clone https://github.com/drMy5tery/Trust-Me-Bro
   ```
3. Install required dependencies using pipenv(navigate to the pipfile folder)
   ```sh
   pipenv install
   ```
4. Activate the virtual environment
   ```sh
   pipenv shell
   ```
5. Ensure that your python interpreter path for your current working project is set to the virtual environment
   ```sh
   python -c "import sys; print(sys.executable)"
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have suggestions for improving the method using better ML models, please reach out to us via email or through the GitHub repository's issues or pull requests. We welcome valid ideas and will consider integrating them into the main project. Please keep in mind that we prefer to utilize free tools and technologies whenever possible.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[contributors-shield]: https://img.shields.io/github/contributors/drMy5tery/Trust-Me-Bro.svg?style=for-the-badge
[contributors-url]: https://github.com/drMy5tery/Trust-Me-Bro/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/drMy5tery/Trust-Me-Bro.svg?style=for-the-badge
[forks-url]: https://github.com/drMy5tery/Trust-Me-Bro/network/members
[stars-shield]: https://img.shields.io/github/stars/drMy5tery/Trust-Me-Bro.svg?style=for-the-badge
[stars-url]: https://github.com/drMy5tery/Trust-Me-Bro/stargazers
[issues-shield]: https://img.shields.io/github/issues/drMy5tery/Trust-Me-Bro.svg?style=for-the-badge
[issues-url]: https://github.com/drMy5tery/Trust-Me-Bro/issues
[license-shield]: https://img.shields.io/github/license/drMy5tery/Trust-Me-Bro.svg?style=for-the-badge
[license-url]: https://github.com/drMy5tery/Trust-Me-Bro/LICENSE.txt
[about-positive]: images/About_positive.png
[Django.com]:https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Javascript.com]: https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E
[Javascript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[Vercel.com]: https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white
[Vercel-url]: https://vercel.com/
[Tailwind.com]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[Tailwind-url]: https://tailwindcss.com/
[YoutubeApi.com]: https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white
[Youtube-api-url]: https://developers.google.com/youtube/v3
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 