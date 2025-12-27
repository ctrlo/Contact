#!/usr/bin/perl

use strict; use warnings;

use DateTime;
use FindBin qw/ $Bin /;
use Plack::Request;
use Plack::Response;

use Mail::Message;

my $app = sub {

    my $req     = Plack::Request->new( shift );
    my $query   = $req->body_parameters;

    my $name      = $query->get('name');
    my $email     = $query->get('email');
    my $telephone = $query->get('telephone');
    my $message   = $query->get('message');

    my $body = << "_BODY";
A new message has been submitted on the website.

Name: $name
Email: $email
Telephone: $telephone

Message: $message

_BODY

    #use Data::Dumper; say STDERR $query->get('submit');
    Mail::Message->build(
        To             => 'info@ctrlo.com',
        From           => 'info@ctrlo.com',
        Subject        => "New contact submission from website",
        data           => $body,
    )->send(via => 'postfix');

    my $res = Plack::Response->new( 200 );
    $res->header('Content-Type' => 'text/plain');
    $res->header('Access-Control-Allow-Origin' => 'https://www.ctrlo.com');
    $res->body('Thank you, your message has been sent');
    $res->finalize;
};

use Plack::Handler::CGI;
Plack::Handler::CGI->new->run($app);
