{
  description = "...";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devshell.url = "github:numtide/devshell";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [inputs.devshell.flakeModule];
      systems = [ "x86_64-linux" "aarch64-linux" ];

      perSystem = { config, self', inputs', pkgs, system, ... }: {
        devshells.default = {
          packages = with pkgs; [
            (python311.withPackages(ps: with ps; [ tkinter ]))
          ];
        };
      };
    };
}
