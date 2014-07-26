#!/usr/bin/perl

use strict;
use warnings;
use CGI;
use Imager;
use LWP::Simple;
use MIME::Base64;
local $| = 1;
use CGI::Carp qw(fatalsToBrowser);


my $q = CGI->new();
my $filename   = time().".png";
my $canvas_b64 = $q->param('canvas'  );
my $image_url  = $q->param('imageurl');
my $referer    = $q->referer();

die unless $referer =~ m|^http://labo.dtpwiki.jp/|;

# canvas_b64 の処理、data:で入ってくるのでチェックしてデコード
my $re = qr/^data:image\/png;base64,/;
die unless ( $canvas_b64 =~ m/$re/ );
$canvas_b64 =~ s/$re//;
my $png_canvas = decode_base64($canvas_b64);

# image_url の処理。URLがhttp:の場合は素直にGET、data:の場合はデコード
my $png_base;
if ( $image_url =~ m/$re/ ) {
  $image_url =~ s/$re//;
  $png_base = decode_base64($image_url);
}
else {
  $LWP::Simple::ua->agent("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)");
  $png_base = get($image_url) or die;
}

my $img_aka  = Imager->new;
my $img_base = Imager->new;
$img_aka ->read( data => $png_canvas, );
$img_base->read( data => $png_base, );
$img_base->rubthrough( src  => $img_aka,);
my $newdata;
$img_base->write( data => \$newdata, type=>'png');

print $q->header(
  -type                => 'image/png',
  -Content_Disposition => 'inline; filename="' . $filename .'"',
  -Access_Control_Allow_Origin => "*"
);
print $newdata;

exit;

__END__


