# JarWiz - Gesture and Action Recognition Software

## Inspiration

The creation of JarWiz was born out of a desire to overcome the limitations of traditional keyboard and mouse inputs, especially in the context of accessibility and user interaction. Witnessing the challenges faced by individuals with motor impairments, and recognizing the potential for gesture recognition to revolutionize computing, we set out to develop a product that empowers users to interact naturally with computers. JarWiz is driven by a vision to make computing more accessible, efficient, and enjoyable for all users, embracing inclusivity and innovation.

## What It Does

"JarWiz" is a groundbreaking gesture and action recognition software that redefines computer accessibility. Liberating users from traditional inputs, it introduces intuitive gestures for seamless control. Beyond accessibility, JarWiz serves as a generic gesture control interface, with applications in various fields, including hardware control and annotation. The technology allows users to operate computers through hand gestures and voice commands, transforming the user experience.

## Demo Video

Check out our [Demo Video](https://youtu.be/hVN4Yjrqk-M) to see JarWiz in action and witness how it revolutionizes the way we interact with technology.

## How We Built It

Our implementation of JarWiz utilizes OpenCV (cv2) to map hand gestures in real time. Computer vision techniques were employed to detect and track hand movements, recognize gestures, and translate them into actionable commands. The integration of Whisper, a cutting-edge speech-to-text library, further enhances the user experience by allowing voice commands alongside gestures. JarWiz not only offers versatile interaction but also supports hardware control, enabling intuitive manipulation through gestures.

## Technologies Used

- OpenCV (cv2)
- Whisper (Speech-to-text library)
- CNN (Convolutional Neural Network)
- Flask
- HTML
- CSS
- MongoDB
- Node.js
- Python
- PyTorch

## Challenges Faced

We encountered specific challenges during the development process, including:

- Real-time audio detection
- Mapping finger positions to the desktop screen for intuitive navigation
- Designing varying yet comfortable gestures for different operations
- Ensuring real-time, lag-free computation with resource-intensive image and action detection algorithms

## Acknowledgments

We would like to acknowledge the support of the open-source community and the contributors who have inspired and shaped the development of JarWiz. Your contributions are invaluable in making computing more accessible and innovative.

Feel free to explore, contribute, and revolutionize the way we interact with technology with JarWiz! 🚀
