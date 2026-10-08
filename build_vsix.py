#!/usr/bin/env python3
import json, os, zipfile

def build():
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, "package.json")) as f:
        pkg = json.load(f)
    vsix_path = os.path.join(root, f"{pkg['name']}-{pkg['version']}.vsix")
    ct = '<?xml version="1.0" encoding="utf-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n  <Default Extension="manifest" ContentType="text/xml" />\n  <Default Extension="vsixmanifest" ContentType="text/xml" />\n  <Default Extension="json" ContentType="application/json" />\n  <Default Extension="md" ContentType="text/markdown" />\n  <Default Extension="txt" ContentType="text/plain" />\n  <Default Extension="xml" ContentType="text/xml" />\n</Types>'
    manifest_tmpl = '<?xml version="1.0" encoding="utf-8"?>\n<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">\n  <Metadata>\n    <Identity Language="en-US" Id="{name}" Version="{ver}" Publisher="{pub}" />\n    <DisplayName>{disp}</DisplayName>\n    <Description xml:space="preserve">{desc}</Description>\n    <Tags>theme,color-theme,dark theme,jetbrains,intellij,islands,pycharm,webstorm</Tags>\n    <Categories>Themes</Categories>\n    <Properties>\n      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.75.0" />\n      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="ui,workspace,web" />\n    </Properties>\n  </Metadata>\n  <Installation>\n    <InstallationTarget Id="Microsoft.VisualStudio.Code" />\n  </Installation>\n  <Dependencies />\n  <Assets>\n    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />\n    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true" />\n  </Assets>\n</PackageManifest>'
    manifest = manifest_tmpl.format(name=pkg["name"], ver=pkg["version"], pub=pkg["publisher"], disp=pkg["displayName"], desc=pkg["description"])
    with zipfile.ZipFile(vsix_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("extension.vsixmanifest", manifest)
        z.write(os.path.join(root, "package.json"), "extension/package.json")
        z.write(os.path.join(root, "README.md"), "extension/README.md")
        themes_dir = os.path.join(root, "themes")
        for fn in os.listdir(themes_dir):
            if fn.endswith(".json"):
                z.write(os.path.join(themes_dir, fn), f"extension/themes/{fn}")
    print(f"Built {vsix_path} successfully!")

if __name__ == "__main__":
    build()
