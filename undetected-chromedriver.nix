{ lib
, buildPythonPackage
, fetchFromGitHub
, selenium
, requests
, websockets
}:
buildPythonPackage rec {
  pname = "undetected-chromedriver";
  version = "3.5.4";

  src = fetchFromGitHub {
    owner = "ultrafunkamsterdam";
    repo = pname;
    rev = "783b8393157b578e19e85b04d300fe06efeef653";
    hash = "sha256-vQ66TAImX0GZCSIaphEfE9O/wMNflGuGB54+29FiUJE=";
  };

  propagatedBuildInputs = [
    selenium
    requests
    websockets
  ];

  #  prePatch = ''
  #  substituteInPlace setup.py \
  #    --replace "selenium>=4.9.0" "selenium"
  #'';

  pythonImportsCheck = [
    "undetected_chromedriver"
  ];

  meta = with lib; {
    homepage = "https://github.com/UltrafunkAmsterdam/undetected-chromedriver";
    changelog = "https://github.com/ultrafunkamsterdam/undetected-chromedriver/blob/master/README.md";
    license = licenses.gpl3Only;
    description = ''
      Selenium.webdriver.Chrome replacement with compatiblity for Brave, and other Chromium based browsers.
      Not triggered by CloudFlare/Imperva/hCaptcha and such.
      NOTE: results may vary due to many factors. No guarantees are given, except for ongoing efforts in understanding detection algorithms.
    '';
    longDescription = ''
      Selenium.webdriver.Chrome replacement with compatiblity for Brave, and other Chromium based browsers.
      Not triggered by CloudFlare/Imperva/hCaptcha and such.
      NOTE: results may vary due to many factors. No guarantees are given, except for ongoing efforts in understanding detection algorithms.
    '';
    maintainers = [ ];
  };
}
