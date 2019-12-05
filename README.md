# Face-Swapping-Images

The facial landmarks are detected using Dlib and 68 facial landmark package. Then the region of the landmarks of first image is subdivided into several triangles and the lanmark points are saved.
The same process is followed with the second image. Each triangle points are taken in two images and then a matrix is formed using Affine Transform function. Then the first triangle of the first image is warped with the first triangle of second image so that the shape of the trianles looks similar. 

Same process is repeated for every triangles so that the face from the first image gets converted into the shape of face of second image. The generated face is then masked with the second image.

Seamless cloning is done to match the color of face of the generated image with the second image body.
