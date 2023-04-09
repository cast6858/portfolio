To run an AI model in UiPath, the following requirements need to be fulfilled:

UiPath Studio: UiPath Studio is an integrated development environment (IDE) used for designing and building automation workflows. It is required to install UiPath Studio on the system where the AI model is to be run.

Enterprise Version: Connect to the enterprise version of UiPath

AI Model: The AI model should be trained and saved in a compatible format. In this case run the train model first and save the pickel data.

Python Libraries: UiPath requires certain Python libraries to interact with AI models. These include Pandas, NLTK, Scikit-learn. Ensure that these libraries are installed in your system.

UiPath ML Activities Package:UiPath requires an ML Activities. This package can be installed from the UiPath Package Manager.


Once all these requirements are fulfilled, you can use UiPath to load the AI model, pass input data, and obtain the output