{ lib, stdenv, fetchzip, autoPatchelfHook, pkgs, libxcb
}:
stdenv.mkDerivation {
  pname = "arm-chromedriver";
  version = "120.0.6099.109";

  src = fetchzip {
    url = "https://github.com/electron/electron/releases/download/v28.1.0/chromedriver-v28.1.0-linux-arm64.zip";
    hash = "sha256-nGOixMfKzhd3ztAvI2KRF3ERIPsrLj7I26qD9hY139A=";
    stripRoot = false; # this .zip is a flat list of files, not a zipped directory
  };

  nativeBuildInputs = [ autoPatchelfHook ];

  buildInputs = with pkgs; [
    stdenv.cc.cc.lib glib libxcb nspr nss
  ];

  installPhase = ''
  runHook preInstall
  install -m777 -D $src/chromedriver $out/bin/chromedriver
  runHook postInstall
  '';

  meta = with lib; {
    description = "ChromeDriver for ARM";
    platforms = [ "aarch64-linux" ];
  };

}
