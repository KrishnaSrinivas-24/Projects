import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import javax.imageio.ImageIO;

public class ImageEncryptDecrypt {

    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("\nChoose an option:");
            System.out.println("1. Encrypt");
            System.out.println("2. Decrypt");
            System.out.println("3. Exit");
            String choice = sc.nextLine();

            switch (choice) {
                case "1":
                    System.out.print("Enter image filename (with extension): ");
                    String inputImage = sc.nextLine();
                    System.out.print("Enter secret message: ");
                    String message = sc.nextLine();
                    System.out.print("Enter encryption key (integer): ");
                    int keyEnc = Integer.parseInt(sc.nextLine());

                    encryptImage(inputImage, message, keyEnc);
                    break;

                case "2":
                    System.out.print("Enter encrypted image filename (with extension): ");
                    String encryptedImage = sc.nextLine();
                    System.out.print("Enter decryption key (integer): ");
                    int keyDec = Integer.parseInt(sc.nextLine());

                    String decryptedMessage = decryptImage(encryptedImage, keyDec);
                    System.out.println("Decrypted Message: " + decryptedMessage);
                    break;

                case "3":
                    System.out.println("Mission Completed \nExiting...");
                    return;

                default:
                    System.out.println("Invalid choice. Try again.");
            }
        }
    }

    private static void encryptImage(String fileName, String message, int key) throws IOException {
        BufferedImage image = ImageIO.read(new File(fileName));
        int width = image.getWidth();
        int height = image.getHeight();

        byte[] msgBytes = message.getBytes();
        int msgLen = msgBytes.length;

        byte[] fullMsg = new byte[msgLen + 4];
        fullMsg[0] = (byte) ((msgLen >> 24) & 0xFF);
        fullMsg[1] = (byte) ((msgLen >> 16) & 0xFF);
        fullMsg[2] = (byte) ((msgLen >> 8) & 0xFF);
        fullMsg[3] = (byte) (msgLen & 0xFF);
        System.arraycopy(msgBytes, 0, fullMsg, 4, msgLen);

        int totalBits = fullMsg.length * 8;
        if (totalBits > width * height * 3) {
            throw new IllegalArgumentException("Message too long for this image.");
        }

        int bitIndex = 0;

        outer:
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int rgb = image.getRGB(x, y);
                int r = (rgb >> 16) & 0xFF;
                int g = (rgb >> 8) & 0xFF;
                int b = rgb & 0xFF;

                r ^= key;
                g ^= key;
                b ^= key;

                if (bitIndex < totalBits) {
                    int byteIndex = bitIndex / 8;
                    int bitPos = 7 - (bitIndex % 8);
                    int bit = (fullMsg[byteIndex] >> bitPos) & 1;
                    r = (r & 0xFE) | bit;
                    bitIndex++;
                }

                int newRGB = (r << 16) | (g << 8) | b;
                image.setRGB(x, y, newRGB);

                if (bitIndex >= totalBits) {
                    break outer;
                }
            }
        }

        ImageIO.write(image, "png", new File("encrypted_image.png"));
        System.out.println("Image encrypted and saved as encrypted_image.png");
    }

    private static String decryptImage(String fileName, int key) throws IOException {
        BufferedImage image = ImageIO.read(new File(fileName));
        int width = image.getWidth();
        int height = image.getHeight();

        byte[] header = new byte[4];
        int bitIndex = 0;

        // Extract the first 4 bytes (message length)
        for (int i = 0; i < 32; i++) {
            int x = (i % width);
            int y = (i / width);
            int rgb = image.getRGB(x, y);
            int r = (rgb >> 16) & 0xFF;
            header[bitIndex / 8] = (byte) ((header[bitIndex / 8] << 1) | (r & 1));
            bitIndex++;
        }

        // Convert header bytes to integer message length
        int msgLen = ((header[0] & 0xFF) << 24)
                | ((header[1] & 0xFF) << 16)
                | ((header[2] & 0xFF) << 8)
                | (header[3] & 0xFF);

        if (msgLen <= 0 || msgLen > width * height) {
            throw new IllegalArgumentException("Invalid message length extracted: " + msgLen);
        }

        byte[] msgBytes = new byte[msgLen];
        int totalBits = msgLen * 8;
        int bitCounter = 0;
        int pixelIndex = 32; // Skip first 4 bytes

        // Extract the message
        for (int i = 0; i < totalBits; i++) {
            int x = ((i + pixelIndex) % width);
            int y = ((i + pixelIndex) / width);
            int rgb = image.getRGB(x, y);
            int r = (rgb >> 16) & 0xFF;

            msgBytes[i / 8] = (byte) ((msgBytes[i / 8] << 1) | (r & 1));
        }

        return new String(msgBytes);
    }
}
