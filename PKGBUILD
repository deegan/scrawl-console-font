# Maintainer: Hakan Bjorklund <hakan.bjorklund@gmail.com>
pkgname=scrawl-console-font
pkgver=1.0.0
pkgrel=1
pkgdesc="Slackware 'scrawl' VGA console font, converted to BDF for use in GUI terminals (e.g. foot), with a foot config fragment"
arch=('any')
url="https://slackware.uk/slackware/slackware64-15.0/slackware64/a/kbd-1.15.3-x86_64-6.txz"
license=('GPL2')
depends=('fontconfig' 'python')
optdepends=('foot: run scrawl-font-setup-foot to wire the font into foot.ini')
install=scrawl-console-font.install
noextract=('scrawl_s.fnt.gz' 'scrawl_w.fnt.gz')
source=('scrawl_s.fnt.gz'
        'scrawl_w.fnt.gz'
        'raw2bdf.py'
        'foot-scrawl.ini'
        'scrawl-font-setup-foot')
sha256sums=('688130b57beccbd23279ea8baba7f939020c04e617081fe93fe77a56137af93b'
            '31d9cf4cd49639870d71d08759f3b681af24bb5d4292cedafb102ac60d9c3d72'
            '5981abcaa43166d1f137a079a82f8ac7caa7cdd08e2dfa1471fe13c38ba08e58'
            'd8575949d5f83d638ba4f81f66d2bca0544ba46ab7eca22701dd5e74a16c3c6a'
            '3ac913bc5f05dd0a5cf3e895c4b14f4f3079d1702ce0f7abefcb7a2bb159170c')

build() {
	cd "$srcdir"
	gzip -dc scrawl_s.fnt.gz > scrawl_s.fnt
	gzip -dc scrawl_w.fnt.gz > scrawl_w.fnt
	python3 raw2bdf.py scrawl_s.fnt ScrawlS.bdf ScrawlS
	python3 raw2bdf.py scrawl_w.fnt ScrawlW.bdf ScrawlW
}

package() {
	install -Dm644 "$srcdir/ScrawlS.bdf" "$pkgdir/usr/share/fonts/scrawl-console/ScrawlS.bdf"
	install -Dm644 "$srcdir/ScrawlW.bdf" "$pkgdir/usr/share/fonts/scrawl-console/ScrawlW.bdf"
	install -Dm644 "$srcdir/foot-scrawl.ini" "$pkgdir/usr/share/scrawl-console-font/foot-scrawl.ini"
	install -Dm755 "$srcdir/scrawl-font-setup-foot" "$pkgdir/usr/bin/scrawl-font-setup-foot"
}
