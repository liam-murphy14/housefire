{
  description = "Nix flake for the python build inputs to housefire";

  # inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.nixpkgs.url = "git+file:///Users/liammurphy/Projects/nixpkgs";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
      housefirePythonServerlessPackage = { callPackage, python3Packages }: callPackage ./default.nix {
        pandas = python3Packages.pandas;
        python-dotenv = python3Packages.python-dotenv;
        requests = python3Packages.requests;
        undetected-chromedriver = python3Packages.undetected-chromedriver;
      };
      housefireServerlessPython = { python3, fetchFromGitHub }: python3.withPackages (ps: with ps; [
        (callPackage ./default.nix {
          pandas = pandas;
          python-dotenv = python-dotenv;
          requests = requests;
          undetected-chromedriver = undetected-chromedriver;
        })
        pandas
        python-dotenv
        black
        requests
        undetected-chromedriver
      ]);
    in
    {
      packages = forEachSupportedSystem ({ pkgs }: {
        default = housefirePythonServerlessPackage {
          callPackage = pkgs.callPackage;
          python3Packages = pkgs.python311Packages;
        };
      });
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            (housefireServerlessPython {
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
