{ stdenv
, lib
, fetchzip
}:

stdenv.mkDerivation {
  pname = "arm-chromedriver";
  version = "120.0.6099.109";

  src = fetchzip {
    url = "https://github.com/electron/electron/releases/download/v28.1.0/chromedriver-v28.1.0-linux-arm64.zip"
      hash = "";
  };

  installPhase = ''
    mkdir -p $out/bin
    cp chromedriver $out/bin'';
  # nativeBuildInputs = [ autoPatchelfHook ];

  # installPhase = ''
  # runHook preInstall
  # install -m755 -D $src/out/Release/chromedriver $out/bin/chromedriver

  # '';

  meta = with lib; {
    description = "ChromeDriver for ARM";
    platforms = [ "aarch64-linux" ];
  };

}
