import pexpect
child = pexpect.spawn ('ftp ftp.openbsd.org')
child.expect ('Name .*: ')
child.sendline ('anonymous')
print "sent ID"
child.expect ('Password:')
child.sendline ('noah@example.com')
print "sent PW"
child.expect ('ftp> ')
child.sendline ('cd pub')
child.expect('ftp> ')
child.sendline ('get ls-lR.gz')
print "get File"
child.expect('ftp> ')
child.sendline ('bye')
print "Exit"

print child.before # Print the result of the ls command.
