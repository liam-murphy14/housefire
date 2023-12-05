{ lib
, buildPythonPackage
, pandas
, redis
, hiredis
, python-dotenv
, requests
, undetected-chromedriver
}:
buildPythonPackage rec {
  pname = "python-scripts-housefire";
  version = "1.0.0";

  src = ./python_scripts_housefire/.;

  propagatedBuildInputs = [
    pandas
    redis
    hiredis
    python-dotenv
    requests
    undetected-chromedriver
  ];

  meta = with lib; {
    homepage = "https://github.com/liam-murphy14/housefire";
    description = "A personal project for people to see REITs";
  };
}
