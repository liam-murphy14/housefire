{ buildPythonPackage
, pythonOlder
, pandas
, python-dotenv
, requests
, nodriver
, setuptools
}:

buildPythonPackage {
  pname = "housefire";
  version = "1.0.0";
  pyproject = true;

  disabled = pythonOlder "3.9";

  src = ./.;

  dependencies = [
    pandas
    python-dotenv
    requests
    nodriver
  ];

  build-system = [ setuptools ];

  meta = {
    homepage = "https://github.com/liam-murphy14/housefire";
    description = "A personal project for people to see REITs";
  };
}
