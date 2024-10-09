from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters)
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
import requests
import mnemonic
import logging
import time
import datetime
import json
import functools
web3 = Web3(Web3.HTTPProvider('https://connect.bit-rock.io/'))  # RPC-URL
BITROCK_API = "https://explorer.bit-rock.io/api/v2"  # BitRockAPI
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
contract_address = "0xeeabd314e2eE640B1aca3B27808972B05c7f6A3b"  # RockRouter Contract Address
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
func = 0
logger = logging.getLogger(__name__)
contract_abi = ('[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address",'
                '"name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],'
                '"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],'
                '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA",'
                '"type":"address"},{"internalType":"address","name":"tokenB","type":"address"},'
                '{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin",'
                '"type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},'
                '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline",'
                '"type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA",'
                '"type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},'
                '{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable",'
                '"type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},'
                '{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin",'
                '"type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
                '"name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256",'
                '"name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH",'
                '"type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],'
                '"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{'
                '"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},'
                '{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256",'
                '"name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut",'
                '"type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn",'
                '"type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256",'
                '"name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},'
                '{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{'
                '"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure",'
                '"type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},'
                '{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{'
                '"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view",'
                '"type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},'
                '{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{'
                '"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view",'
                '"type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},'
                '{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256",'
                '"name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256",'
                '"name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{'
                '"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address",'
                '"name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},'
                '{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},'
                '{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{'
                '"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                '"internalType":"address","name":"token","type":"address"},{"internalType":"uint256",'
                '"name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin",'
                '"type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},'
                '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline",'
                '"type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256",'
                '"name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH",'
                '"type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                '"internalType":"address","name":"token","type":"address"},{"internalType":"uint256",'
                '"name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin",'
                '"type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},'
                '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline",'
                '"type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{'
                '"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable",'
                '"type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},'
                '{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin",'
                '"type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
                '"name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},'
                '{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r",'
                '"type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],'
                '"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken",'
                '"type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],'
                '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address",'
                '"name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},'
                '{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},'
                '{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool",'
                '"name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},'
                '{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s",'
                '"type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{'
                '"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable",'
                '"type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},'
                '{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256",'
                '"name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin",'
                '"type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},'
                '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline",'
                '"type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8",'
                '"name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},'
                '{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit",'
                '"outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                '"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]",'
                '"name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},'
                '{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens",'
                '"outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],'
                '"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256",'
                '"name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address['
                ']"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
                '"name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{'
                '"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable",'
                '"type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},'
                '{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to",'
                '"type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],'
                '"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],'
                '"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256",'
                '"name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin",'
                '"type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},'
                '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline",'
                '"type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]",'
                '"name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                '"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address['
                ']"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
                '"name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens",'
                '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256",'
                '"name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin",'
                '"type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},'
                '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline",'
                '"type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]",'
                '"name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                '"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address['
                ']"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
                '"name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens",'
                '"outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256",'
                '"name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax",'
                '"type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},'
                '{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline",'
                '"type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]",'
                '"name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{'
                '"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256",'
                '"name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address['
                ']"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256",'
                '"name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{'
                '"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable",'
                '"type":"function"},{"stateMutability":"payable","type":"receive"}]')
sellAbi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "CanNotModifyMainPair",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "LimitsRemovedAlready",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "MaxFeeLimitExceeded",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "UpdateBoolValue",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "value",
                "type": "bool"
            }
        ],
        "name": "ExcludedFromFees",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "buyFee",
                "type": "uint16"
            },
            {
                "indexed": False,
                "internalType": "uint16",
                "name": "sellFee",
                "type": "uint16"
            }
        ],
        "name": "FeesUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "lp",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "value",
                "type": "bool"
            }
        ],
        "name": "NewLPUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "BURN",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "MAX_FEE",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "burnFeeBuy",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "burnFeeSell",
        "outputs": [
            {
                "internalType": "uint16",
                "name": "",
                "type": "uint16"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "subtractedValue",
                "type": "uint256"
            }
        ],
        "name": "decreaseAllowance",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "isExcluded",
                "type": "bool"
            }
        ],
        "name": "excludeFromFees",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "addedValue",
                "type": "uint256"
            }
        ],
        "name": "increaseAllowance",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "isExcludedFromFees",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "isLiquidityPair",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newPair",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "value",
                "type": "bool"
            }
        ],
        "name": "manageLiquidityPairs",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "removeLimits",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "uniswapV2Pair",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "uniswapV2Router",
        "outputs": [
            {
                "internalType": "contract IUniswapV2Router02",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint16",
                "name": "buy",
                "type": "uint16"
            },
            {
                "internalType": "uint16",
                "name": "sell",
                "type": "uint16"
            }
        ],
        "name": "updateFees",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
token_contract_abi = json.loads(
    '[	{	"inputs": [	{	"internalType": "uint256",	"name": "userinput_buy_liquidity_fee",	"type": "uint256"	'
    '},	{	"internalType": "uint256",	"name": "userinput_buy_marketing_fee",	"type": "uint256"	},	'
    '{	"internalType": "uint256",	"name": "userinput_sell_liquidity_fee",	"type": "uint256"	},	'
    '{	"internalType": "uint256",	"name": "userinput_sell_marketing_fee",	"type": "uint256"	},	'
    '{	"internalType": "uint256",	"name": "userinput_max_tx_percent",	"type": "uint256"	},	{	"internalType": '
    '"uint256",	"name": "userinput_max_wallet_percent",	"type": "uint256"	},	{	"internalType": "uint256",	'
    '"name": "userinput_totalsupply",	"type": "uint256"	},	{	"internalType": "string",	"name": '
    '"userinput_token_name",	"type": "string"	},	{	"internalType": "string",	"name": '
    '"userinput_token_symbol",	"type": "string"	},	{	"internalType": "address",	"name": '
    '"userinput_marketingaddress",	"type": "address"	}	],	"stateMutability": "nonpayable",	"type": '
    '"constructor"	},	{	"anonymous": false,	"inputs": [	{	"indexed": true,	"internalType": "address",	'
    '"name": "owner",	"type": "address"	},	{	"indexed": true,	"internalType": "address",	"name": '
    '"spender",	"type": "address"	},	{	"indexed": false,	"internalType": "uint256",	"name": "value",	'
    '"type": "uint256"	}	],	"name": "Approval",	"type": "event"	},	{	"anonymous": false,	"inputs": [],	'
    '"name": "AutoNukeLP",	"type": "event"	},	{	"anonymous": false,	"inputs": [	{	"indexed": true,	'
    '"internalType": "address",	"name": "sniper",	"type": "address"	}	],	"name": "BoughtEarly",	'
    '"type": "event"	},	{	"anonymous": false,	"inputs": [	{	"indexed": true,	"internalType": "address",	'
    '"name": "newWallet",	"type": "address"	},	{	"indexed": true,	"internalType": "address",	'
    '"name": "oldWallet",	"type": "address"	}	],	"name": "Dev_WalleteloperUpdated",	"type": "event"	},	'
    '{	"anonymous": false,	"inputs": [	{	"indexed": true,	"internalType": "address",	"name": "account",	'
    '"type": "address"	},	{	"indexed": false,	"internalType": "bool",	"name": "isExcluded",	"type": "bool"	'
    '}	],	"name": "ExcludeFromFees",	"type": "event"	},	{	"anonymous": false,	"inputs": [],	'
    '"name": "ManualNukeLP",	"type": "event"	},	{	"anonymous": false,	"inputs": [	{	"indexed": true,	'
    '"internalType": "address",	"name": "newWallet",	"type": "address"	},	{	"indexed": true,	'
    '"internalType": "address",	"name": "oldWallet",	"type": "address"	}	],	"name": '
    '"Marketing_WalletUpdated",	"type": "event"	},	{	"anonymous": false,	"inputs": [	{	"indexed": true,	'
    '"internalType": "address",	"name": "previousOwner",	"type": "address"	},	{	"indexed": true,	'
    '"internalType": "address",	"name": "newOwner",	"type": "address"	}	],	"name": "OwnershipTransferred",	'
    '"type": "event"	},	{	"anonymous": false,	"inputs": [	{	"indexed": true,	"internalType": "address",	'
    '"name": "pair",	"type": "address"	},	{	"indexed": true,	"internalType": "bool",	"name": "value",	'
    '"type": "bool"	}	],	"name": "SetAutomatedMarketMakerPair",	"type": "event"	},	{	"anonymous": false,	'
    '"inputs": [	{	"indexed": false,	"internalType": "uint256",	"name": "tokensSwapped",	"type": '
    '"uint256"	},	{	"indexed": false,	"internalType": "uint256",	"name": "ethReceived",	"type": "uint256"	'
    '},	{	"indexed": false,	"internalType": "uint256",	"name": "tokensIntoLiquidity",	"type": "uint256"	}	'
    '],	"name": "SwapAndLiquify",	"type": "event"	},	{	"anonymous": false,	"inputs": [	{	"indexed": true,	'
    '"internalType": "address",	"name": "from",	"type": "address"	},	{	"indexed": true,	"internalType": '
    '"address",	"name": "to",	"type": "address"	},	{	"indexed": false,	"internalType": "uint256",	'
    '"name": "value",	"type": "uint256"	}	],	"name": "Transfer",	"type": "event"	},	{	"anonymous": false,	'
    '"inputs": [	{	"indexed": true,	"internalType": "address",	"name": "newAddress",	"type": "address"	'
    '},	{	"indexed": true,	"internalType": "address",	"name": "oldAddress",	"type": "address"	}	],	'
    '"name": "UpdateUniswapV2Router",	"type": "event"	},	{	"inputs": [],	"name": "Buy_Liquidity_Fee",	'
    '"outputs": [	{	"internalType": "uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": '
    '"view",	"type": "function"	},	{	"inputs": [],	"name": "Buy_Marketing_Fee",	"outputs": [	{	'
    '"internalType": "uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": "view",	'
    '"type": "function"	},	{	"inputs": [],	"name": "Buy_Total_Fees",	"outputs": [	{	"internalType": '
    '"uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": "view",	"type": "function"	},	'
    '{	"inputs": [],	"name": "Enable_Trading",	"outputs": [],	"stateMutability": "nonpayable",	'
    '"type": "function"	},	{	"inputs": [],	"name": "Limits_In_Effect",	"outputs": [	{	"internalType": '
    '"bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "view",	"type": "function"	},	{	"inputs": '
    '[],	"name": "Marketing_Wallet",	"outputs": [	{	"internalType": "address",	"name": "",	"type": '
    '"address"	}	],	"stateMutability": "view",	"type": "function"	},	{	"inputs": [],	"name": '
    '"Max_Transaction_Amount",	"outputs": [	{	"internalType": "uint256",	"name": "",	"type": "uint256"	}	'
    '],	"stateMutability": "view",	"type": "function"	},	{	"inputs": [],	"name": "Max_Wallet_Amount",	'
    '"outputs": [	{	"internalType": "uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": '
    '"view",	"type": "function"	},	{	"inputs": [],	"name": "Remove_Limits",	"outputs": [	{	'
    '"internalType": "bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "nonpayable",	'
    '"type": "function"	},	{	"inputs": [],	"name": "Renounce_Ownership",	"outputs": [],	"stateMutability": '
    '"nonpayable",	"type": "function"	},	{	"inputs": [],	"name": "RockswapV2Pair",	"outputs": [	{	'
    '"internalType": "address",	"name": "",	"type": "address"	}	],	"stateMutability": "view",	'
    '"type": "function"	},	{	"inputs": [],	"name": "RockswapV2Router",	"outputs": [	{	"internalType": '
    '"contract IUniswapV2Router02",	"name": "",	"type": "address"	}	],	"stateMutability": "view",	'
    '"type": "function"	},	{	"inputs": [],	"name": "Sell_Liquidity_Fee",	"outputs": [	{	"internalType": '
    '"uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": "view",	"type": "function"	},	'
    '{	"inputs": [],	"name": "Sell_Marketing_Fee",	"outputs": [	{	"internalType": "uint256",	"name": "",	'
    '"type": "uint256"	}	],	"stateMutability": "view",	"type": "function"	},	{	"inputs": [],	'
    '"name": "Sell_Total_Fees",	"outputs": [	{	"internalType": "uint256",	"name": "",	"type": "uint256"	}	'
    '],	"stateMutability": "view",	"type": "function"	},	{	"inputs": [],	"name": "Swap_Enabled",	"outputs": '
    '[	{	"internalType": "bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "view",	'
    '"type": "function"	},	{	"inputs": [],	"name": "Swap_Threshold_Amount",	"outputs": [	{	'
    '"internalType": "uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": "view",	'
    '"type": "function"	},	{	"inputs": [],	"name": "Trading_Active",	"outputs": [	{	"internalType": '
    '"bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "view",	"type": "function"	},	{	"inputs": '
    '[	{	"internalType": "uint256",	"name": "_marketingFee",	"type": "uint256"	},	{	"internalType": '
    '"uint256",	"name": "_liquidityFee",	"type": "uint256"	}	],	"name": "Update_Buy_Fees",	"outputs": [],	'
    '"stateMutability": "nonpayable",	"type": "function"	},	{	"inputs": [	{	"internalType": "uint256",	'
    '"name": "newNum",	"type": "uint256"	}	],	"name": "Update_Max_Tx_Amount",	"outputs": [],	"stateMutability": '
    '"nonpayable",	"type": "function"	},	{	"inputs": [	{	"internalType": "uint256",	"name": "newNum",	'
    '"type": "uint256"	}	],	"name": "Update_Max_Wallet_Amount",	"outputs": [],	"stateMutability": '
    '"nonpayable",	"type": "function"	},	{	"inputs": [	{	"internalType": "uint256",	"name": '
    '"_marketingFee",	"type": "uint256"	},	{	"internalType": "uint256",	"name": "_liquidityFee",	'
    '"type": "uint256"	}	],	"name": "Update_Sell_Fees",	"outputs": [],	"stateMutability": "nonpayable",	'
    '"type": "function"	},	{	"inputs": [	{	"internalType": "bool",	"name": "enabled",	"type": "bool"	}	],	'
    '"name": "Update_Swap_Enabled",	"outputs": [],	"stateMutability": "nonpayable",	"type": "function"	},	'
    '{	"inputs": [	{	"internalType": "uint256",	"name": "newAmount",	"type": "uint256"	}	],	'
    '"name": "Update_Threshold_Amount",	"outputs": [	{	"internalType": "bool",	"name": "",	"type": "bool"	}	'
    '],	"stateMutability": "nonpayable",	"type": "function"	},	{	"inputs": [	{	"internalType": "address",	'
    '"name": "owner",	"type": "address"	},	{	"internalType": "address",	"name": "spender",	"type": '
    '"address"	}	],	"name": "allowance",	"outputs": [	{	"internalType": "uint256",	"name": "",	'
    '"type": "uint256"	}	],	"stateMutability": "view",	"type": "function"	},	{	"inputs": [	{	'
    '"internalType": "address",	"name": "spender",	"type": "address"	},	{	"internalType": "uint256",	'
    '"name": "amount",	"type": "uint256"	}	],	"name": "approve",	"outputs": [	{	"internalType": "bool",	'
    '"name": "",	"type": "bool"	}	],	"stateMutability": "nonpayable",	"type": "function"	},	{	"inputs": '
    '[	{	"internalType": "address",	"name": "account",	"type": "address"	}	],	"name": "balanceOf",	'
    '"outputs": [	{	"internalType": "uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": '
    '"view",	"type": "function"	},	{	"inputs": [],	"name": "decimals",	"outputs": [	{	"internalType": '
    '"uint8",	"name": "",	"type": "uint8"	}	],	"stateMutability": "view",	"type": "function"	},	{	"inputs": '
    '[	{	"internalType": "address",	"name": "spender",	"type": "address"	},	{	"internalType": "uint256",	'
    '"name": "subtractedValue",	"type": "uint256"	}	],	"name": "decreaseAllowance",	"outputs": [	{	'
    '"internalType": "bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "nonpayable",	'
    '"type": "function"	},	{	"inputs": [	{	"internalType": "address",	"name": "account",	"type": "address"	'
    '},	{	"internalType": "bool",	"name": "excluded",	"type": "bool"	}	],	"name": "excludeFromFees",	"outputs": '
    '[],	"stateMutability": "nonpayable",	"type": "function"	},	{	"inputs": [	{	"internalType": '
    '"address",	"name": "updAds",	"type": "address"	},	{	"internalType": "bool",	"name": "isEx",	'
    '"type": "bool"	}	],	"name": "excludeFromMaxTransaction",	"outputs": [],	"stateMutability": '
    '"nonpayable",	"type": "function"	},	{	"inputs": [	{	"internalType": "address",	"name": "spender",	'
    '"type": "address"	},	{	"internalType": "uint256",	"name": "addedValue",	"type": "uint256"	}	],	'
    '"name": "increaseAllowance",	"outputs": [	{	"internalType": "bool",	"name": "",	"type": "bool"	}	],	'
    '"stateMutability": "nonpayable",	"type": "function"	},	{	"inputs": [	{	"internalType": "address",	'
    '"name": "account",	"type": "address"	}	],	"name": "isExcludedFromFees",	"outputs": [	{	'
    '"internalType": "bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "view",	"type": "function"	'
    '},	{	"inputs": [],	"name": "name",	"outputs": [	{	"internalType": "string",	"name": "",	'
    '"type": "string"	}	],	"stateMutability": "view",	"type": "function"	},	{	"inputs": [],	'
    '"name": "owner",	"outputs": [	{	"internalType": "address",	"name": "",	"type": "address"	}	],	'
    '"stateMutability": "view",	"type": "function"	},	{	"inputs": [],	"name": "symbol",	"outputs": [	{	'
    '"internalType": "string",	"name": "",	"type": "string"	}	],	"stateMutability": "view",	'
    '"type": "function"	},	{	"inputs": [],	"name": "totalSupply",	"outputs": [	{	"internalType": '
    '"uint256",	"name": "",	"type": "uint256"	}	],	"stateMutability": "view",	"type": "function"	},	'
    '{	"inputs": [	{	"internalType": "address",	"name": "recipient",	"type": "address"	},	'
    '{	"internalType": "uint256",	"name": "amount",	"type": "uint256"	}	],	"name": "transfer",	"outputs": '
    '[	{	"internalType": "bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "nonpayable",	'
    '"type": "function"	},	{	"inputs": [	{	"internalType": "address",	"name": "sender",	"type": "address"	'
    '},	{	"internalType": "address",	"name": "recipient",	"type": "address"	},	{	"internalType": '
    '"uint256",	"name": "amount",	"type": "uint256"	}	],	"name": "transferFrom",	"outputs": [	{	'
    '"internalType": "bool",	"name": "",	"type": "bool"	}	],	"stateMutability": "nonpayable",	'
    '"type": "function"	},	{	"inputs": [	{	"internalType": "address",	"name": "newOwner",	"type": "address"	'
    '}	],	"name": "transferOwnership",	"outputs": [],	"stateMutability": "nonpayable",	"type": "function"	'
    '},	{	"inputs": [	{	"internalType": "address",	"name": "newMarketing_Wallet",	"type": "address"	}	],	'
    '"name": "updateMarketing_Wallet",	"outputs": [],	"stateMutability": "nonpayable",	"type": "function"	},	'
    '{	"stateMutability": "payable",	"type": "receive"	}	]')
# token_out_address = ""
[INPUT, INPUT1, INPUT2, INPUT3, INPUT4, INPUT5] = range(1, 7)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return
    else:
        await update.message.reply_text("🤩 This is the official BitRock Sniper Bot 🔫 deployed by @bitdogbrock 🤩")
        return


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return
    Account.enable_unaudited_hdwallet_features()
    mnemonic_phrase = mnemonic.Mnemonic("english").generate()
    account = Account.from_mnemonic(mnemonic_phrase)
    key = account.key.hex()
    address = account.address
    response_message = f"<b>🥳 PHRASE WORD :</b>\n<code>{mnemonic_phrase}</code>\n\n"
    response_message += f"<b>🥳 PRIVATE KEY :</b>\n<code>{key}</code>\n\n"
    response_message += f"<b>🥳 ADDRESS :</b>\n<code>{address}</code>\n\n"
    response_message += "⚠️ Remember to keep your phrase words and private key safe! ⚠️"
    await update.message.reply_text(response_message, parse_mode="HTML")
    await update.message.reply_text("😇 Now use /add_wallet to add this wallet 😇")


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = context.user_data
    if 'wallet_connected' not in user_data:
        user_data['wallet_connected'] = False
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return
    if not user_data['wallet_connected']:
        await update.effective_message.reply_text("😊 Please connect your wallet before checking the balance, "
                                                  "add wallet using /add_wallet command 😊")
        return
    result = ""
    for addresses in range(0, len(user_data['private_key_values'])):
        connected_wallet_address = Account.from_key(user_data['private_key_values'][addresses])
        BitRock_address = connected_wallet_address.address
        BitRock_url = f"{BITROCK_API}/addresses/{BitRock_address}"
        response = requests.get(BitRock_url, verify=False)
        if response.status_code == 200:
            BitRock_data = response.json()
            coin_balance_raw = BitRock_data.get("coin_balance", "N/A")
            if coin_balance_raw != "N/A":
                coin_balance = int(coin_balance_raw) / 10 ** 18
                exchange_rate = float(BitRock_data.get("exchange_rate", 0))
                usd_value = coin_balance * exchange_rate
                result_message = (
                    f"💀 Wallet {addresses + 1}:\nBitRock balance for {BitRock_address}: {coin_balance:.8f} BROCK\n"
                    f"USD value: ${usd_value:.2f}"
                )
                result += result_message
                result += "\n\n"
            else:
                result += "❌ Wallet {addresses + 1}: \nBitRock balance not available."
                result += "\n\n"

        else:
            result += f"❌ Wallet {addresses + 1}: \nError code: {response.status_code}"
            result += "\n\n"
    await update.message.reply_text(result)


async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    private_key = update.message.text
    if private_key not in user_data['private_key_values']:
        try:
            account = Account.from_key(private_key)
            user_data['private_key_values'].append(private_key)
            user_data['wallet_connected'] = True
            await update.message.reply_text(f"✅ Wallet {len(user_data['private_key_values'])} Added, Wallet Address: {account.address}")
            return ConversationHandler.END
        except Exception as E:
            await update.message.reply_text(f"Error: {E}")
            return ConversationHandler.END
    else:
        await update.message.reply_text(f"✅ Wallet Already Added")
        return ConversationHandler.END


async def input_connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return ConversationHandler.END
    await update.message.reply_text("😇 Please enter your private key.")
    return INPUT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return ConversationHandler.END
    await update.message.reply_text("❌ Transaction Cancelled")
    return ConversationHandler.END


async def contract_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return ConversationHandler.END
    try:
        user_data['token_out_address'] = update.message.text.strip()
        api_url = f"{BITROCK_API}/addresses/{user_data['token_out_address']}"
        response = requests.get(api_url, verify=False)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            name = data.get("token", {}).get("name", "N/A")
            symbol = data.get("token", {}).get("symbol", "N/A")
            supply = data.get("total_supply", {}).get("symbol", "N/A")
            creator_address = data.get("creator_address_hash", "N/A")
            decimals = data.get("token", {}).get("decimals", "N/A")
            cb = data.get("has_token_transfers")
            vf = data.get("is_verified")
            link_dex = f"https://www.dextools.io/app/en/bitrock/pair-explorer/{user_data['token_out_address']}"
            link_screen = f"https://explorer.bit-rock.io/address/{user_data['token_out_address']}"

            total_holders = data.get("token", {}).get("holders", "N/A")
            # type1 = data.get("token", {}).get("type", "N/A")
            response_message = f"<b>🫡Contract Name:</b> {name}\n"
            response_message += f"<b>☺️Symbol:</b> {symbol}\n"
            # response_message += f"<b>🫣Type:</b> {type1}\n"
            response_message += f"<b>😎Owner Address:</b> <code>{creator_address}</code>\n"
            response_message += f"<b>☺️Decimals:</b> {decimals}\n"
            response_message += f"<b>🫡Total Holders:</b> {total_holders}\n"
            response_message += f"<b>💀Total Supply:</b> {supply}\n"
            response_message += f"<b>😎Token Transfers:</b> {'✅' if cb else '❌'}\n"
            response_message += f"<b>🤩Verified:</b> {'✅' if vf else '❌'}\n\n\n"
            response_message += f"<a href='{link_dex}'>Chart 📈</a>\t\t\t\t<a href='{link_screen}'>Detail 👀</a>\n"

            keyboard = [
                [InlineKeyboardButton("📈 Buy(Spend 100 Brock)", callback_data='buy_100'),
                 InlineKeyboardButton("📈 Buy(Spend 250 Brock)", callback_data='buy_250')],
                [InlineKeyboardButton("📈 Buy(Spend 500 Brock)", callback_data='buy_500'),
                 InlineKeyboardButton("📈 Buy(Spend X Brock)", callback_data='buy_x')],
                [InlineKeyboardButton("📉 Sell 100 Tokens", callback_data='sell_100'),
                 InlineKeyboardButton("📉 Sell 250 Tokens", callback_data='sell_250')],
                [InlineKeyboardButton("📉 Sell 500 Tokens", callback_data='sell_500'),
                 InlineKeyboardButton("📉 Sell X Tokens", callback_data='sell_x')],
                [InlineKeyboardButton("👀 Snipe Liquidity", callback_data='snipe_liquidity'),
                 InlineKeyboardButton("👀 Snipe Trading", callback_data='snipe_trading')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(response_message, parse_mode='HTML', reply_markup=reply_markup)
        else:
            await update.message.reply_text("❌ Error fetching contract details")
        return ConversationHandler.END
    except Exception as E:
        await update.message.reply_text(f"❌ Error: {E}")
        return ConversationHandler.END


async def input_snipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return ConversationHandler.END
    if user_data['private_key_values']:
        await update.message.reply_text("🫡 Enter Token Contract Address: ")
        return INPUT1
    else:
        await update.message.reply_text("⚠️ Add a wallet to perform this, use /add_wallet to add wallet ⚠️")
        return ConversationHandler.END


def execute_sell(context, amount):
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    if 'token_out_address' not in user_data:
        user_data['token_out_address'] = ""
    try:
        tokenValue = web3.to_wei(amount, 'ether')
        token_in_address = web3.to_checksum_address("0x413f0e3a440aba7a15137f4278121450416882d5")
        contract_address_2 = '0xeeabd314e2eE640B1aca3B27808972B05c7f6A3b'
        Account.enable_unaudited_hdwallet_features()
        result = ""
        w = 1
        for private_key_2 in user_data['private_key_values']:
            account = Account.from_key(private_key_2)
            wallet_address = account.address
            contract = web3.eth.contract(address=web3.to_checksum_address(contract_address_2), abi=contract_abi)
            tx = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                tokenValue, 0,
                [Web3.to_checksum_address(user_data['token_out_address']), token_in_address],
                wallet_address,
                (int(time.time()) + 3421831762)

            ).build_transaction({
                'from': wallet_address,
                'gas': 400000,
                'gasPrice': web3.to_wei('30', 'gwei'),
                'nonce': web3.eth.get_transaction_count(web3.to_checksum_address(wallet_address)),
            })
            signed_txn = web3.eth.account.sign_transaction(tx, private_key=private_key_2)
            try:
                tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                result += f"Wallet {w}:\nTransaction Hash: {tx_hash.hex()}\n\n"
                w += 1
            except ValueError as E:
                result += f"Wallet {w}: Error on Transaction: Insufficient Balance\n\n"
                w += 1
        return [0, result]
    except ValueError as E:
        return [1, E]


def execute_trade(context, amount):
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    if 'token_out_address' not in user_data:
        user_data['token_out_address'] = ""
    try:
        token_in_address = web3.to_checksum_address("0x413f0e3a440aba7a15137f4278121450416882d5")
        tokens = [token_in_address, web3.to_checksum_address(user_data['token_out_address'])]
        contract_address_2 = '0xeeabd314e2eE640B1aca3B27808972B05c7f6A3b'
        Account.enable_unaudited_hdwallet_features()
        result = ""
        w = 1
        for private_key_2 in user_data['private_key_values']:
            account = Account.from_key(private_key_2)
            wallet_address = account.address
            nonce = web3.eth.get_transaction_count(web3.to_checksum_address(wallet_address))
            recipient = wallet_address
            deadline = (int(time.time()) + 1709456541)
            contract = web3.eth.contract(address=web3.to_checksum_address(contract_address_2), abi=contract_abi)

            tx = contract.functions.swapExactETHForTokens(
                10000000000000,
                tokens,
                recipient,
                deadline
            ).build_transaction({
                'from': wallet_address,
                'value': web3.to_wei(amount, 'ether'),
                'gas': 2500000,
                'gasPrice': web3.to_wei('5', 'gwei'),
                'nonce': nonce,
            })

            signed_tx = web3.eth.account.sign_transaction(tx, private_key_2)

            try:
                tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                result += f"Wallet {w}: Transaction Hash: {tx_hash.hex()}\n\n"
                w += 1
            except ValueError as E:
                result += f"Wallet {w}: Error on Transaction: Insufficient Balance\n\n"
                w += 1
        return [0, result]
    except ValueError as E:
        return [1, E]


async def buy_token_x(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not await check_membership(update, context):
    #     await update.message.reply_text("Please Join Our Community @bitdogbrock to use this bot")
    #     return ConversationHandler.END
    amount = update.message.text.strip()
    now = datetime.datetime.now()
    ans = execute_trade(context, amount)
    keyboard = [
        [InlineKeyboardButton("📈 Buy(Spend 100 Brock)", callback_data='buy_100'),
         InlineKeyboardButton("📈 Buy(Spend 250 Brock)", callback_data='buy_250')],
        [InlineKeyboardButton("📈 Buy(Spend 500 Brock)", callback_data='buy_500'),
         InlineKeyboardButton("📈 Buy(Spend X Brock)", callback_data='buy_x')],
        [InlineKeyboardButton("📉 Sell 100 Tokens", callback_data='sell_100'),
         InlineKeyboardButton("📉 Sell 250 Tokens", callback_data='sell_250')],
        [InlineKeyboardButton("📉 Sell 500 Tokens", callback_data='sell_500'),
         InlineKeyboardButton("📉 Sell X Tokens", callback_data='sell_x')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if ans[0] == 0:
        await update.message.reply_text(
            f"✅ Buy Executed\n{ans[1]} {now.time()}", parse_mode='HTML', reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(f"❌ Error : {ans[1]}")
        return ConversationHandler.END


async def buy_token(update: Update, context: ContextTypes.DEFAULT_TYPE, amount):
    # if not await check_membership(update, context):
    #     await update.message.reply_text("Please Join Our Community @bitdogbrock to use this bot")
    #     return ConversationHandler.END
    now = datetime.datetime.now()
    ans = execute_trade(context, amount)
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("📈 Buy(Spend 100 Brock)", callback_data='buy_100'),
         InlineKeyboardButton("📈 Buy(Spend 250 Brock)", callback_data='buy_250')],
        [InlineKeyboardButton("📈 Buy(Spend 500 Brock)", callback_data='buy_500'),
         InlineKeyboardButton("📈 Buy(Spend X Brock)", callback_data='buy_x')],
        [InlineKeyboardButton("📉 Sell 100 Tokens", callback_data='sell_100'),
         InlineKeyboardButton("📉 Sell 250 Tokens", callback_data='sell_250')],
        [InlineKeyboardButton("📉 Sell 500 Tokens", callback_data='sell_500'),
         InlineKeyboardButton("📉 Sell X Tokens", callback_data='sell_x')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if ans[0] == 0:
        await query.message.reply_text(
            f"✅ Buy Executed\n{ans[1]}{now.time()}", parse_mode='HTML', reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await query.message.reply_text(f"❌ Error : {ans[1]}")
        return ConversationHandler.END


async def sell_token_x(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not await check_membership(update, context):
    #     await update.message.reply_text("Please Join Our Community @bitdogbrock to use this bot")
    #     return ConversationHandler.END
    amount = update.message.text.strip()
    now = datetime.datetime.now()
    ans = execute_sell(context, amount)
    keyboard = [
        [InlineKeyboardButton("📈 Buy(Spend 100 Brock)", callback_data='buy_100'),
         InlineKeyboardButton("📈 Buy(Spend 250 Brock)", callback_data='buy_250')],
        [InlineKeyboardButton("📈 Buy(Spend 500 Brock)", callback_data='buy_500'),
         InlineKeyboardButton("📈 Buy(Spend X Brock)", callback_data='buy_x')],
        [InlineKeyboardButton("📉 Sell 100 Tokens", callback_data='sell_100'),
         InlineKeyboardButton("📉 Sell 250 Tokens", callback_data='sell_250')],
        [InlineKeyboardButton("📉 Sell 500 Tokens", callback_data='sell_500'),
         InlineKeyboardButton("📉 Sell X Tokens", callback_data='sell_x')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if ans[0] == 0:
        await update.message.reply_text(
            f"✅ Sell Executed\n{ans[1]} {now.time()}", parse_mode='HTML', reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(f"❌ Error : {ans[1]}")
        return ConversationHandler.END


async def sell_token(update: Update, context: ContextTypes.DEFAULT_TYPE, amount):
    # if not await check_membership(update, context):
    #     await update.message.reply_text("Please Join Our Community @bitdogbrock to use this bot")
    #     return ConversationHandler.END
    now = datetime.datetime.now()
    ans = execute_sell(context, amount)
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("📈 Buy(Spend 100 Brock)", callback_data='buy_100'),
         InlineKeyboardButton("📈 Buy(Spend 250 Brock)", callback_data='buy_250')],
        [InlineKeyboardButton("📈 Buy(Spend 500 Brock)", callback_data='buy_500'),
         InlineKeyboardButton("📈 Buy(Spend X Brock)", callback_data='buy_x')],
        [InlineKeyboardButton("📉 Sell 100 Tokens", callback_data='sell_100'),
         InlineKeyboardButton("📉 Sell 250 Tokens", callback_data='sell_250')],
        [InlineKeyboardButton("📉 Sell 500 Tokens", callback_data='sell_500'),
         InlineKeyboardButton("📉 Sell X Tokens", callback_data='sell_x')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if ans[0] == 0:
        await query.message.reply_text(
            f"✅ Sell Executed\n{ans[1]}{now.time()}", parse_mode='HTML', reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await query.message.reply_text(f"❌ Error : {ans[1]}")
        return ConversationHandler.END


async def snipe_loop(context: ContextTypes.DEFAULT_TYPE):
    current_jobs = context.job_queue.jobs()
    # print(current_jobs)
    update = context.job.data['update']
    token_contract = context.job.data['token_contract']
    amount = context.job.data['amount']
    name = context.job.data['name']
    context1 = context.job.data['context']
    flag = context.job.data['flag']
    liquidity_active = token_contract.functions.Swap_Enabled
    trading_active = token_contract.functions.Trading_Active().call()
    if flag == "TD":
        if trading_active:
            ans = execute_trade(context1, amount)
            if ans[0] == 0:
                now = datetime.datetime.now()
                current_jobs = context.job_queue.get_jobs_by_name(name)
                for job in current_jobs:
                    job.schedule_removal()
                await update.message.reply_text(f"✅🫡 Snipe Executed\n{ans[1]}{now.time()}")
            else:
                await update.message.reply_text(f"❌ Error while Sniping: {ans[1]}")
    else:
        if liquidity_active:
            ans = execute_trade(context1, amount)
            if ans[0] == 0:
                now = datetime.datetime.now()
                current_jobs = context.job_queue.get_jobs_by_name(name)
                for job in current_jobs:
                    job.schedule_removal()
                await update.message.reply_text(f"✅🫡 Snipe Executed\n{ans[1]}{now.time()}")
            else:
                await update.message.reply_text(f"❌ Error while Sniping: {ans[1]}")


async def snipe(update: Update, context: ContextTypes.DEFAULT_TYPE, flag):
    global func
    user_data = context.user_data
    if 'token_out_address' not in user_data:
        user_data['token_out_address'] = ""

    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return ConversationHandler.END
    try:
        amount = update.message.text.strip()
        now = datetime.datetime.now()
        token_contract = web3.eth.contract(address=web3.to_checksum_address(user_data['token_out_address']), abi=token_contract_abi)
        await update.message.reply_text(f"✅👀 Snipe Activated at {now.time()} for the token : {user_data['token_out_address']}")
        if web3.is_connected():
            pass
        else:
            return ConversationHandler.END
        context.job_queue.run_repeating(snipe_loop, interval=0.1, name=str(func), data={
            'update': update,
            'token_contract': token_contract,
            'amount': amount,
            'context': context,
            'name': str(func),
            'flag': flag
        })
        func += 1

    except Exception as e:
        await update.message.reply_text(f"❌ Error : {e}")
        return ConversationHandler.END
    return ConversationHandler.END


async def input_amount_sell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    if 'token_out_address' not in user_data:
        user_data['token_out_address'] = ""
    sellTokenContract = web3.eth.contract(web3.to_checksum_address(user_data['token_out_address']), abi=sellAbi)
    result = ""
    w = 1
    symbol = ""
    for private in user_data['private_key_values']:
        account = Account.from_key(private)
        wallet_address = account.address
        balance1 = sellTokenContract.functions.balanceOf(wallet_address).call()
        symbol = sellTokenContract.functions.symbol().call()
        readable = web3.from_wei(balance1, 'ether')
        approve = sellTokenContract.functions.approve(web3.to_checksum_address(user_data['token_out_address']), balance1).build_transaction({
            'from': wallet_address,
            'gas': 250000,
            'gasPrice': web3.to_wei('5', 'gwei'),
            'nonce': web3.eth.get_transaction_count(wallet_address),
        })
        signed_txn = web3.eth.account.sign_transaction(approve, private_key=private)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        result += f"💀 Wallet {w} Balance: " + str(readable) + " " + symbol + "\n" + f"Approved: {web3.to_hex(tx_token)}" "\n\n"
        w += 1
    query = update.callback_query
    await query.message.reply_text(result + f"😎 Enter Amount of {symbol} you want to sell: ")
    return INPUT2


async def input_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # if not await check_membership(update, context):
    #     await update.message.reply_text("Please Join Our Community @bitdogbrock to use this bot")
    #     return ConversationHandler.END
    query = update.callback_query
    await query.message.reply_text("😎 Enter Amount (In Brock) to Spend: ")
    return INPUT2


async def view_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return
    result = ""
    w = 1
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    if user_data['private_key_values']:
        for private in user_data['private_key_values']:
            account = Account.from_key(private)
            wallet_address = account.address
            result += f"💀 Wallet {w}: {wallet_address}\n"
            w += 1
    else:
        result = "⚠️ No wallet added, use /add_wallet to add wallets ⚠️"
    await update.message.reply_text(result)
    return


async def delete_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return ConversationHandler.END
    address = update.message.text.strip()
    flag = False
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    for i in user_data['private_key_values']:
        account = Account.from_key(i)
        wallet_address = account.address
        if address == wallet_address:
            user_data['private_key_values'].remove(i)
            flag = True
    if flag:
        await update.message.reply_text("⚠️ Wallet Deleted Successfully ⚠️")
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Given Wallet not found ❌")
        return ConversationHandler.END


async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member("@bitdogbrock", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking membership: {e}")
        return False


async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.message.from_user.id
    if not await is_user_member(user_id, context):
        return False
    return True


async def delete_wallet_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if 'private_key_values' not in user_data:
        user_data['private_key_values'] = []
    if not await check_membership(update, context):
        await update.message.reply_text("😇 Please Join Our Community @bitdogbrock to use this bot 😇")
        return ConversationHandler.END
    if user_data['private_key_values']:
        await update.message.reply_text("🫣 Enter Wallet Address of the Wallet to delete:")
    else:
        await update.message.reply_text("⚠️ No Wallet Added, use /add_wallet to add wallets  ️⚠️")
        return ConversationHandler.END
    return INPUT5


def main() -> None:
    application = Application.builder().token("6819042741:AAFFpkwaRXeSl3kp-rgM7nX-6WypMQv8Au8").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("view_wallets", view_wallets))
    application.add_handler(CallbackQueryHandler(functools.partial(buy_token, amount=100), pattern='^buy_100'))
    application.add_handler(CallbackQueryHandler(functools.partial(buy_token, amount=250), pattern='^buy_250'))
    application.add_handler(CallbackQueryHandler(functools.partial(buy_token, amount=500), pattern='^buy_500'))
    application.add_handler(CallbackQueryHandler(functools.partial(sell_token, amount=100), pattern='^sell_100'))
    application.add_handler(CallbackQueryHandler(functools.partial(sell_token, amount=250), pattern='^sell_250'))
    application.add_handler(CallbackQueryHandler(functools.partial(sell_token, amount=500), pattern='^sell_500'))

    conversation1 = ConversationHandler(
        entry_points=[CommandHandler('add_wallet', input_connect)],
        states={
            INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, connect)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    conversation2 = ConversationHandler(
        entry_points=[CommandHandler('snipe', input_snipe), CommandHandler('contract_info', input_snipe)],
        states={
            INPUT1: [MessageHandler(filters.TEXT & ~filters.COMMAND, contract_info)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    conversation3 = ConversationHandler(
        entry_points=[CallbackQueryHandler(input_amount, pattern='^snipe_liquidity')],
        states={
            INPUT2: [MessageHandler(filters.TEXT & ~filters.COMMAND, functools.partial(snipe, flag="LQ"))],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    conversation4 = ConversationHandler(
        entry_points=[CallbackQueryHandler(input_amount, pattern='^snipe_trading')],
        states={
            INPUT2: [MessageHandler(filters.TEXT & ~filters.COMMAND, functools.partial(snipe, flag="TD"))],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    conversation5 = ConversationHandler(
        entry_points=[CallbackQueryHandler(input_amount, pattern='^buy_x')],
        states={
            INPUT2: [MessageHandler(filters.TEXT & ~filters.COMMAND, buy_token_x)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    conversation6 = ConversationHandler(
        entry_points=[CallbackQueryHandler(input_amount_sell, pattern='^sell_x')],
        states={
            INPUT2: [MessageHandler(filters.TEXT & ~filters.COMMAND, sell_token_x)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    conversation7 = ConversationHandler(
        entry_points=[CommandHandler('delete_wallet', delete_wallet_ip)],
        states={
            INPUT5: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_wallet)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conversation1)
    application.add_handler(conversation2)
    application.add_handler(conversation3)
    application.add_handler(conversation4)
    application.add_handler(conversation5)
    application.add_handler(conversation6)
    application.add_handler(conversation7)
    application.run_polling()
    application.stop()


if __name__ == "__main__":
    main()
