#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

int main() {
	Mat img = imread("C:\\Users\\GABO\\Desktop\\a.jpg");

	if (img.empty()) {
		cout << "No se cargo la imagen" << endl;
		return -1;
	}

	const size_t canales = 3;
	for (int x = 0; x < img.rows; x++) {
		for (int y = 0; y < img.rows; y++) {
			size_t p = y * img.cols * canales + x * canales;
			uchar b = img.data[p + 0];
			uchar g = img.data[p + 1];
			uchar r = img.data[p + 2];

			img.data[p + 0] = 0;
			img.data[p + 0] = 0;
			img.data[p + 0] = r;
		}
	}

	namedWindow("imagen", WINDOW_AUTOSIZE);
	imshow("imagen", img);

	waitKey();
	return 0;
}