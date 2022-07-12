%define oname RBDOOM-3-BFG

Summary:	Doom 3: BFG Edition game engine
Name:		rbdoom3-bfg
Version:	1.0.3
Release:	6
License:	GPLv3+
Group:		Games/Arcade
Url:		https://github.com/RobertBeckebans/RBDOOM-3-BFG
# https://github.com/RobertBeckebans/RBDOOM-3-BFG/archive/v%{version}.tar.gz
Source0:	%{oname}-%{version}.tar.gz
Source1:	%{name}.png
# Don't override CXX flags
Patch0:		rbdoom3-bfg-1.0.2-cflags.patch
Patch1:		rbdoom3-bfg-1.0.2-static.patch
Patch2:		rbdoom3-bfg-1.0.3-path.patch
Patch3:		rbdoom3-bfg-1.0.3-ffmpeg29.patch
Patch4:		rbdoom3-bfg-1.0.3-gcc7.patch
Patch5:		rbdoom3-bfg-1.0.3-gcc8.patch
Patch6:		rbdoom3-bfg-1.0.3-c++14.patch
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:	ffmpeg-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(zlib)
Provides:	%{oname} = %{EVRD}
Provides:	doom3-bfg = %{version}

%description
Doom 3: BFG Edition game engine with soft shadows, cleaned up source, Linux
and 64 bit support.

WARNING! Playing Doom 3: BFG Edition still requires a legitimate copy of
the game. You can purchase a copy from Steam or your favorite retailer.

Place "base" folder from the Doom 3 installation to:
%{_gamesdatadir}/%{name}/
or
$HOME/.rbdoom3bfg/

%files
%doc README.txt COPYING.txt
%{_gamesbindir}/%{name}
%dir %attr(0777,root,root) %{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{oname}-%{version}

%build
%global optflags %{optflags} -std=c++14
pushd neo
%cmake
%make
popd

%install
mkdir -p %{buildroot}%{_gamesbindir}
install -m 0755 neo/build/RBDoom3BFG %{buildroot}%{_gamesbindir}/%{name}

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Doom 3: BFG Edition
Comment=A first-person science fiction horror video game
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

# install menu icons
for N in 16 32 48 64 128;
do
convert %{SOURCE1} -scale ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

mkdir -p %{buildroot}%{_gamesdatadir}/%{name}