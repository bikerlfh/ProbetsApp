#!/bin/bash

cd /tmp/
if [[ "$EB_IS_COMMAND_LEADER" == "true" ]]; then
    # leader
  sudo wget https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
  sudo unzip chromedriver_linux64.zip
  sudo mv chromedriver /usr/bin/chromedriver

  sudo curl https://intoli.com/install-google-chrome.sh | bash
  sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
fi
