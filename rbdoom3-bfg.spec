%define oname RBDOOM-3-BFG

Summary:	Doom 3: BFG Edition game engine
Name:		rbdoom3-bfg
Version:	1.4.0
Release:	1
License:	GPLv3+
Group:		Games/Arcade
Url:		https://github.com/RobertBeckebans/RBDOOM-3-BFG
Source0:	https://github.com/RobertBeckebans/RBDOOM-3-BFG/archive/refs/tags/v%{version}/%{oname}-%{version}.tar.gz
Source1:	%{name}.png
BuildRequires:	cmake
BuildRequires:	imagemagick
BuildRequires:  rapidjson
BuildRequires:	ffmpeg-devel
BuildRequires:	jpeg-devel
BuildRequires:  pkgconfig(libpng)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:  pkgconfig(glew)
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
#export CC=gcc
#export CXX=g++
pushd neo
%cmake  \
  -DBUILD_SHARED_LIBS=OFF \
  -DSDL2=ON \
  -DOPENAL=ON \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DONATIVE=OFF \
  -DUSE_SYSTEM_ZLIB=ON \
  -DUSE_SYSTEM_LIBPNG=ON \
  -DUSE_SYSTEM_LIBJPEG=ON \
  -DUSE_SYSTEM_LIBGLEW=ON \
  -DUSE_SYSTEM_RAPIDJSON=ON
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
