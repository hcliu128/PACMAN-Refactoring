# python -m unittest test_pacman.py -v
import unittest
from unittest.mock import MagicMock, patch
import pygame
from character.Player import Player
from character.Ghost import Ghost
from utils.Block import Block
from utils.Settings import Blinky_directions, Inky_directions, Clyde_directions, Pinky_directions, pl, bl, il, cl
from utils.Wall import Wall
import utils.Colors as Colors
from utils.init import initialize

class TestPacman(unittest.TestCase):
    def setUp(self):
        print("setUp...")
        pygame.init()
        # 創建一個假環境
        self.screen = pygame.display.set_mode((1, 1))
        self.walls = pygame.sprite.Group()

        # 創建一面牆
        self.wall = Wall(100, 100, 50, 50, (0, 0, 255))
        self.walls.add(self.wall)

        # 創建一個玩家
        self.player = Player(90, 90, "images/Trollman.png")
    
    def tearDown(self):
        print("tearDown...")
        pygame.quit()

    @patch("pygame.sprite.spritecollide")
    def test_player_moves_correctly(self, mock_spritecollide):
        # 模擬 spritecollide 返回空列表（無碰撞）
        mock_spritecollide.return_value = []

        # 玩家改變方向
        self.player.changespeed(10, 0)  # 向右移動
        self.player.update(self.walls, False)

        # 確認玩家位置已更新
        self.assertEqual(self.player.rect.left, 100)
        self.assertEqual(self.player.rect.top, 90)

    @patch("pygame.sprite.spritecollide")
    def test_player_collides_with_wall(self, mock_spritecollide):
        # 模擬 spritecollide 返回牆的列表（表示碰撞）
        mock_spritecollide.return_value = [self.wall]

        # 記錄原始位置
        original_x = self.player.rect.left
        original_y = self.player.rect.top

        # 玩家嘗試向右移動，但撞牆
        self.player.changespeed(10, 0)
        self.player.update(self.walls, False)

        # 確認玩家位置未更新
        self.assertEqual(self.player.rect.left, original_x)
        self.assertEqual(self.player.rect.top, original_y)

if __name__ == "__main__":
    unittest.main()
