{ lib
, buildPythonPackage
, pandas
, python-dotenv
, requests
, undetected-chromedriver
, chromium
}:

buildPythonPackage rec {
  pname = "python-serverless-housefire";
  version = "1.0.0";

  src = ./.;

  propagatedBuildInputs = [
    pandas
    python-dotenv
    requests
    undetected-chromedriver
  ];

  buildInputs = [ chromium ];

  meta = with lib; {
    homepage = "https://github.com/liam-murphy14/housefire";
    description = "A personal project for people to see REITs";
  };
}
