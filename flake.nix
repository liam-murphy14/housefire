{
  description = "Nix flake for the python build inputs to housefire";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
      housefirePython = { python3, fetchFromGitHub }: python3.withPackages (ps: with ps; [
        (callPackage ./default.nix {
          pandas = pandas;
          redis = redis;
          hiredis = hiredis;
          python-dotenv = python-dotenv;
          requests = requests;
          undetected-chromedriver = (callPackage ./undetected-chromedriver.nix {
            selenium = selenium;
            requests = requests;
            websockets = websockets;
          });
        })
        pandas
        redis
        hiredis
        python-dotenv
        black
        requests
        (callPackage ./undetected-chromedriver.nix {
          selenium = selenium;
          requests = requests;
          websockets = websockets;
        })
      ]);
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            (housefirePython {
              python3 = python311;
              fetchFromGitHub = fetchFromGitHub;
            })
          ];
        };
      });
      formatter = forEachSupportedSystem ({ pkgs }: pkgs.nixpkgs-fmt
      );

    };
}
