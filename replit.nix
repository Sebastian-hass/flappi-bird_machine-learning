{ pkgs }: {
  deps = [
    pkgs.python39Full
    pkgs.python39Packages.pip
    pkgs.python39Packages.pygame
    pkgs.python39Packages.numpy
  ];
}
