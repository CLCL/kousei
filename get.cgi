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
my $image_url  = $q->param('imageurl');
my $referer    = $q->referer();

#die unless $referer =~ m|^http://labo.dtpwiki.jp/|;

# image_url の処理。URLがhttp:の場合は素直にGET、data:の場合はデコード
my $png_base;
my $re = qr/^data:image\/png;base64,/;
my $newdata;
my $newdata_base;
if ( $image_url =~ m/$re/ ) {
  $newdata_base = $image_url;
}
else {
  $LWP::Simple::ua->agent("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)");
  $png_base = get($image_url) or die;
  my $img_base = Imager->new;
  $img_base->read( data => $png_base, );
  $img_base->write( data => \$newdata, type=>'png');
  $newdata_base = 'data:image/png;base64,' .encode_base64($newdata) ;
}

print $q->header(
  -type => 'image/png',
);
print $newdata;

exit;

__END__


