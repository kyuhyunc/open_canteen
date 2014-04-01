#!/usr/bin/perl -w

open(FILE,"<foodlist.txt");
while(<FILE>) {
	if ($_ =~ m/$ARGV[0]/) {
		print;
	}
}
close(FILE);
