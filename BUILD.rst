RFDoc
=====

Releasing a new version
-----------------------

1. Update the VERSION identifier

    Edit 'src/rfdoc/version.py' in the source repo and commit.

2. Tag the source repo and push it

    hg tag N.N && hg push

3. Create a source .tar.gz distribution

    python setup.py sdist --formats=gztar

    Verify that the content looks correct:

        tar -ztvf rfdoc-N.N.tar.gz

4. Upload the source distribution to PyPi

    python setup.py sdist upload

5. Update the 'News' section at https://code.google.com/p/rfdoc to mention
   about the release with short description of what was done.

    Done via https://code.google.com/p/rfdoc/admin.
