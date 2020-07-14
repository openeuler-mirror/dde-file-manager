Name:           dde-file-manager
Version:        5.1.2.3
Release:        7
Summary:        Deepin File Manager
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-file-manager
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  deepin-gettext-tools
BuildRequires:  dde-dock-devel
BuildRequires:  file-devel
#BuildRequires:  jemalloc-devel
#BuildRequires:  cmake(KF5Codecs)
BuildRequires:  pkgconfig(atk)
BuildRequires:  dtkgui-devel
BuildRequires:  pkgconfig(dtkwidget) >= 5.1
BuildRequires:  pkgconfig(dframeworkdbus) >= 2.0
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(poppler-cpp)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-qt5-1)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires:  pkgconfig(taglib)
#BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  qt5-linguist
BuildRequires:  jemalloc-devel
#BuildRequires:  udisks2-qt5
BuildRequires:  udisks2-qt5-devel
BuildRequires:  disomaster-devel
BuildRequires:  libgio-qt libgio-qt-devel
BuildRequires:  openssl-devel
BuildRequires:  libqtxdg-devel
BuildRequires:  libmediainfo-devel
BuildRequires:  kf5-kcodecs-devel
#BuildRequires:  libudisks2-qt5-devel

# run command by QProcess
#Requires:       deepin-shortcut-viewer
Requires:       deepin-terminal
Requires:       dde-desktop
Requires:       file-roller
#Requires:       gvfs-client
#Requires:       samba
#Requires:       xdg-user-dirs
#Requires:       gstreamer-plugins-good
Recommends:     deepin-manual

%description
File manager front end of Deepin OS.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%package -n libdde-file-manager
Summary:        DDE File Manager library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n libdde-file-manager
DDE File Manager library.

%package -n dde-disk-mount-plugin
Summary:        plugin of dde-dock
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n dde-disk-mount-plugin
plugin of dde-dock.

%package -n dde-desktop
Summary:        Deepin desktop environment - desktop module
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       dde-dock
Requires:       dde-launcher
Requires:       dde-session-ui

%description -n dde-desktop
Deepin desktop environment - desktop module.

%prep
%setup -q -n %{name}-%{version}

# fix file permissions
find -type f -perm 775 -exec chmod 644 {} \;
#sed -i '/target.path/s|lib|%{_lib}|' dde-dock-plugins/disk-mount/disk-mount.pro
sed -i '/deepin-daemon/s|lib|libexec|' dde-zone/mainwindow.h
sed -i 's|lib/gvfs|libexec|' %{name}-lib/gvfs/networkmanager.cpp
#sed -i 's|%{_datadir}|%{_libdir}|' dde-sharefiles/appbase.pri
sed -i 's|/lib/dde-dock/plugins|/lib64/dde-dock/plugins|' dde-dock-plugins/disk-mount/disk-mount.pro

%build
export PATH=%{_qt5_bindir}:$PATH
%qmake_qt5 PREFIX=%{_prefix} QMAKE_CFLAGS_ISYSTEM= CONFIG+="DISABLE_FFMPEG DISABLE_ANYTHING"
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/dde-computer.desktop ||:
desktop-file-validate %{buildroot}%{_datadir}/applications/dde-trash.desktop ||:

%ldconfig_scriptlets

%files
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.deepin.filemanager.daemon.conf
%{_bindir}/%{name}
%{_bindir}/%{name}-daemon
%{_bindir}/%{name}-pkexec
%{_bindir}/dde-property-dialog
/usr/lib/systemd/system/dde-filemanager-daemon.service
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/interfaces/com.deepin.filemanager.filedialog.xml
%{_datadir}/dbus-1/interfaces/com.deepin.filemanager.filedialogmanager.xml
%{_datadir}/dbus-1/services/com.deepin.filemanager.filedialog.service
%{_datadir}/dbus-1/services/org.freedesktop.FileManager.service
%{_datadir}/dbus-1/system-services/com.deepin.filemanager.daemon.service
%{_polkit_qt_policydir}/com.deepin.filemanager.daemon.policy
%{_polkit_qt_policydir}/com.deepin.pkexec.dde-file-manager.policy

%files -n libdde-file-manager
%{_libdir}/dde-file-manager/plugins/previews/libdde-image-preview-plugin.so
%{_libdir}/dde-file-manager/plugins/previews/libdde-music-preview-plugin.so
%{_libdir}/dde-file-manager/plugins/previews/libdde-pdf-preview-plugin.so
%{_libdir}/dde-file-manager/plugins/previews/libdde-text-preview-plugin.so
%{_libdir}/libdde-file-manager.so.1.8.2
%{_datadir}/dde-file-manager/mimetypeassociations/mimetypeassociations.json
%{_datadir}/dde-file-manager/mimetypes/archive.mimetype
%{_datadir}/dde-file-manager/mimetypes/audio.mimetype
%{_datadir}/dde-file-manager/mimetypes/backup.mimetype
%{_datadir}/dde-file-manager/mimetypes/executable.mimetype
%{_datadir}/dde-file-manager/mimetypes/image.mimetype
%{_datadir}/dde-file-manager/mimetypes/text.mimetype
%{_datadir}/dde-file-manager/mimetypes/video.mimetype
%{_datadir}/dde-file-manager/templates/newDoc.doc
%{_datadir}/dde-file-manager/templates/newExcel.xls
%{_datadir}/dde-file-manager/templates/newPowerPoint.ppt
%{_datadir}/dde-file-manager/templates/newTxt.txt
%{_datadir}/dde-file-manager/translations/
%{_datadir}/deepin/dde-file-manager/oem-menuextensions/.readme
%{_datadir}/glib-2.0/schemas/com.deepin.dde.filemanager.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/dde-file-manager.svg
%{_libdir}/libdde-file-manager.so.1
%{_libdir}/libdde-file-manager.so.1.8

%files -n dde-disk-mount-plugin
%{_libdir}/dde-dock/plugins/system-trays/libdde-disk-mount-plugin.so
%{_datadir}/dde-disk-mount-plugin/translations
%{_datadir}/glib-2.0/schemas/com.deepin.dde.dock.module.disk-mount.gschema.xml




%files devel
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/gvfs/
%{_includedir}/%{name}/%{name}-plugins/
%{_includedir}/%{name}/private/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%files -n dde-desktop
%{_bindir}/dde-desktop
%{_datadir}/applications/dde-computer.desktop
%exclude %{_datadir}/applications/dde-open.desktop
%{_datadir}/applications/dde-trash.desktop
%dir %{_datadir}/dde-desktop
%{_datadir}/dde-desktop/translations/
%{_datadir}/dbus-1/services/com.deepin.dde.desktop.service

%changelog
* Mon Jul 06 2020 uoser <uoser@uniontech.com> - 5.1.2.3-7
- Move plug-in library to /usr/lib64 directory

* Thu Sep 26 2019 Jan Grulich <jgrulich@redhat.com> - 4.7.7-5
- rebuild (qt5)

* Mon Jun 17 2019 Jan Grulich <jgrulich@redhat.com> - 4.7.7-4
- rebuild (qt5)

* Mon Jun 10 2019 Robin Lee <cheeselee@fedoraproject.org> - 4.7.7-3
- rebuild (Qt5)

* Sun Mar 10 2019 Robin Lee <cheeselee@fedoraproject.org> - 4.7.7-2
- rebuild (Qt5)

* Tue Feb 26 2019 mosquito <sensor.wen@gmail.com> - 4.7.7-1
- Update to 4.7.7

* Tue Feb 19 2019 mosquito <sensor.wen@gmail.com> - 4.7.6-1
- Update to 4.7.6

* Thu Jan 31 2019 mosquito <sensor.wen@gmail.com> - 4.7.5-1
- Update to 4.7.5

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 23 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.10-1
- Update to 4.7.1.10

* Tue Dec 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.7.1.9-2
- rebuild (Qt5)

* Thu Dec 13 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.9-1
- Update to 4.7.1.9

* Thu Dec 13 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.7.1.4-2
- rebuild (qt5)

* Thu Nov 29 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.4-1
- Update to 4.7.1.4

* Thu Nov 22 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.1-2
- Add Req deepin-session-ui, deepin-dock, deepin-launcher

* Mon Nov 12 2018 mosquito <sensor.wen@gmail.com> - 4.7.1.1-1
- Update to 4.7.1.1

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 4.4.9.1-2
- rebuild (qt5)

* Wed Aug 15 2018 mosquito <sensor.wen@gmail.com> - 4.4.9.1-1
- Update to 4.4.9.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-10
- rebuild (qt5)

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-9
- rebuild (qt5)

* Fri Mar 23 2018 Marek Kasik <mkasik@redhat.com> - 4.4.7-8
- Rebuild for poppler-0.63.0

* Mon Mar 19 2018 mosquito <sensor.wen@gmail.com> - 4.4.7-7
- Exclude ppc64le, ppc64, aarch64

* Sat Mar 10 2018 mosquito <sensor.wen@gmail.com> - 4.4.7-6
- Remove obsoletes statement (BZ#1537223)

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-5
- rebuild (qt5)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.7-3
- Remove obsolete scriptlets

* Mon Jan 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 4.4.7-2
- rebuild (qt5)

* Sat Dec  2 2017 mosquito <sensor.wen@gmail.com> - 4.4.7-1
- Update to 4.4.7

* Mon Nov 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-2
- rebuild (qt5)

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 4.3.4-1
- Update to 4.3.4

* Fri Oct 13 2017 mosquito <sensor.wen@gmail.com> - 4.3.2-1
- Update to 4.3.2
- Remove ffmpeg patch file
- BR: Qt5Concurrent Qt5DBus Qt5Gui

* Wed Oct 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 4.2.5-2
- BR: qt5-qtbase-private-devel

* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 4.2.5-1
- Update to 4.2.5

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 4.2.4-1
- Update to 4.2.4

* Sun Aug 20 2017 mosquito <sensor.wen@gmail.com> - 4.2.3-1
- Update to 4.2.3

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 4.2.2-1
- Update to 4.2.2

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.1.8-1.git9308953
- Update to 4.1.8

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.1.5-1.git99d7597
- Update to 4.1.5

* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 1.4.1-1.gite303113
- Update to 1.4.1

* Sat Jan 28 2017 mosquito <sensor.wen@gmail.com> - 1.3.8-1.git207000d
- Update to 1.3.8

* Sun Jan 22 2017 mosquito <sensor.wen@gmail.com> - 1.3.7-2.gitf1915f8
- Add Req for run command

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.3.7-1.gitf1915f8
- Update to 1.3.7

* Thu Jan 12 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-3
- Fixed broken icon link noticed by Brenton Horne <brentonhorne77@gmail.com>

* Fri Jan 06 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-2
- Fixed build dependecies

* Fri Dec 30 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-1
- Update package to 1.3.6 and rename to deepin-file-manager

* Mon Dec 19 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.4-1
- Update package to 1.3.4

* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.3-1
- Update package to 1.3.3

* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.3-1
- Initial package build
