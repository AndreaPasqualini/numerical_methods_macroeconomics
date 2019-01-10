# Numerical Methods in Macroeconomics

## Setting up Python for Data Science (and Macro)

These are instructions you might want to follow if you want to set up your local machine (e.g., your laptop) to run Python.
I will also include details about the main packages we need.

The following instructions hold for Windows, Mac OS and Linux.


### Installing Python through Anaconda

Python alone cannot do much.
It's a bit like installing a new OS on a computer: can you do stuff with it?
Yes, but not much: you'll need additional applications.
With Python, we need [modules](https://docs.python.org/3/tutorial/modules.html).

As [it is not easy to manage modules](https://en.wikipedia.org/wiki/Dependency_hell) manually, we're going to need a [package manager](https://en.wikipedia.org/wiki/Package_manager).
The one we choose for this setup is [Anaconda](https://www.anaconda.com/), which is popular among people who need to do numerical and stastical work (some prefer calling it data science).

Go to https://www.anaconda.com/download/ and download the file that is relevant for your OS.
You should choose the Python 3.x version, as the 2.x is [legacy (read: old) software](https://en.wikipedia.org/wiki/Legacy_system) that is there for compatibility (i.e., targeting audiences different from us).
You can find instructions on how to install Anaconda for [Windows](https://docs.anaconda.com/anaconda/install/windows/), [macOS](https://docs.anaconda.com/anaconda/install/mac-os/) and [Linux](https://docs.anaconda.com/anaconda/install/linux/).

As the typical Anaconda installation includes all the packages we'll need (including the Python interpreter), **we're done**.
To confirm this is the case, search for [Spyder](https://www.spyder-ide.org/) among your applications and launch it: this will be our [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment) for the rest of the course.

If one day you want to get rid of Anaconda, you can just follow the [instructions to uninstall](https://docs.anaconda.com/anaconda/install/uninstall/) it.

Anaconda by default installs the most common packages typical "data scientists" use.
We are not going to use all of them in this course.
If you're very mindful about your computer and you're interested in having a leaner installation, read the [README for pros](./README_pro.md).
You're also going to find extra software you might want to check out.


