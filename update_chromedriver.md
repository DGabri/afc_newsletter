How to update chromedriver

version=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE")
echo "Installing ChromeDriver for version $version"
wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${version}/linux64/chromedriver-linux64.zip -O /tmp/chromedriver-linux64.zip
sudo unzip -oj /tmp/chromedriver-linux64.zip -d /usr/bin

sudo chmod 755 /usr/bin/chromedriver
chromedriver --version