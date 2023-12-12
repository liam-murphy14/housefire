{
  description = "Nix flake for the python build inputs to housefire";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
      housefirePythonScriptsPackage = { callPackage, python3Packages }: callPackage ./default.nix {
        pandas = python3Packages.pandas;
        redis = python3Packages.redis;
        hiredis = python3Packages.hiredis;
        python-dotenv = python3Packages.python-dotenv;
        requests = python3Packages.requests;
        undetected-chromedriver = (callPackage ./undetected-chromedriver.nix {
          selenium = python3Packages.selenium;
          requests = python3Packages.requests;
          websockets = python3Packages.websockets;
        });
      };
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
      packages = forEachSupportedSystem ({ pkgs }: {
        default = housefirePythonScriptsPackage {
          callPackage = pkgs.callPackage;
          python3Packages = pkgs.python311Packages;
        };
      });
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
