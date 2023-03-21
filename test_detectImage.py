import unittest
import detectImage

class TestDetectImage(unittest.TestCase):

    def test_enable_alert(self):
        detectImage.cooldownList = ['targets/discord_text.png', 'targets/discord.png']
        detectImage.finalFileList = ['targets/discord.png', 'targets/firewall.png']
        detectImage.enable_alert()
        self.assertEqual(detectImage.finalFileList, ['targets/discord.png', 'targets/firewall.png', 'targets/discord_text.png'])
        self.assertEqual(detectImage.cooldownList, ['targets/discord.png'])
        
    def test_scanimage(self):
        filepath = 'targets/firewall.png'
        """detectImage.img_gray = 'gray scale image'"""
        detectImage.img = 'targets/firewall.png'
        detectImage.finalFileList = ['targets/firewall.png']
        detectImage.cooldownList = []
        detectImage.cooldownCount = 0
        detectImage.timer = []
        detectImage.scanimage(filepath)
        self.assertEqual(len(detectImage.finalFileList), 0)
        self.assertEqual(len(detectImage.cooldownList), 1)
        self.assertEqual(detectImage.cooldownList[0], 'targets/firewall.png')

if __name__ == '__main__':
    unittest.main()
