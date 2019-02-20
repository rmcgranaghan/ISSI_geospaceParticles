{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2019-02-20T16:19:48.664171Z",
     "start_time": "2019-02-20T16:19:47.016037Z"
    }
   },
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "from datetime import timedelta, datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2019-02-20T16:19:49.116808Z",
     "start_time": "2019-02-20T16:19:49.108407Z"
    }
   },
   "outputs": [],
   "source": [
    "def hist6hr(data):\n",
    "    hr6 = [data[i-timedelta(hours=6.5):i-timedelta(hours=5.5)].mean().values\n",
    "           for i in data.index]\n",
    "    columns = [i+'_6hr' for i in data.columns]\n",
    "    return pd.DataFrame(hr6, index=data.index,columns=columns)\n",
    "\n",
    "def hist5hr(data):\n",
    "    hr5 = [data[i-timedelta(hours=5.5):i-timedelta(hours=4.5)].mean().values\n",
    "           for i in data.index]\n",
    "    columns = [i+'5hr' for i in data.columns]\n",
    "    return pd.DataFrame(hr5, index=data.index,columns=columns)\n",
    "\n",
    "def hist3hr(data):\n",
    "    hr3 = [data[i-timedelta(hours=3.25):i-timedelta(hours=2.75)].mean().values\n",
    "           for i in data.index]\n",
    "    columns = [i+'_3hr' for i in data.columns]\n",
    "    return pd.DataFrame(hr3, index=data.index,columns=columns)\n",
    "\n",
    "def hist1hr(data):\n",
    "    hr1 = [data[i-timedelta(hours=1.25):i-timedelta(hours=0.75)].mean().values\n",
    "           for i in data.index]\n",
    "    columns = [i+'_1hr' for i in data.columns]\n",
    "    return pd.DataFrame(hr1, index=data.index,columns=columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2019-02-20T16:19:49.164262Z",
     "start_time": "2019-02-20T16:19:49.141410Z"
    }
   },
   "outputs": [],
   "source": [
    "def hist45min(data):\n",
    "    min45 = [data.loc[i-timedelta(minutes=45)].values\n",
    "             for i in data.index\n",
    "             if i >= data.index[0]+timedelta(minutes=45)]\n",
    "    columns = [i+'_45min' for i in data.columns]\n",
    "    return pd.DataFrame(min45, index=data.index[int(45/5):],columns=columns)\n",
    "\n",
    "def hist30min(data):\n",
    "    min30 = [data.loc[i-timedelta(hours=0.5)].values\n",
    "             for i in data.index\n",
    "             if i >= data.index[0]+timedelta(minutes=30)]\n",
    "    columns = [i+'_30min' for i in data.columns]\n",
    "    return pd.DataFrame(min30, index=data.index[int(30/5):],columns=columns)\n",
    "\n",
    "def hist15min(data):\n",
    "    min15 = [data.loc[i-timedelta(hours=0.25)].values\n",
    "             for i in data.index\n",
    "             if i >= data.index[0]+timedelta(minutes=15)]\n",
    "    columns = [i+'_15min' for i in data.columns]\n",
    "    return pd.DataFrame(min15, index=data.index[int(15/5):],columns=columns)\n",
    "\n",
    "def hist10min(data):\n",
    "    min10 = [data.loc[i-timedelta(minutes=10)].values\n",
    "             for i in data.index\n",
    "             if i >= data.index[0]+timedelta(minutes=10)]\n",
    "    columns = [i+'_10min' for i in data.columns]\n",
    "    return pd.DataFrame(min10, index=data.index[int(10/5):],columns=columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2019-02-20T16:44:27.348049Z",
     "start_time": "2019-02-20T16:44:27.341236Z"
    },
    "scrolled": false
   },
   "outputs": [],
   "source": [
    "def time_history(data):\n",
    "    '''\n",
    "    Function which calculates time history information\n",
    "    given an input dataframe.\n",
    "    \n",
    "    Averages are centred on the respective time-history\n",
    "    specified.\n",
    "    \n",
    "    Input:\n",
    "    data - a Pandas DataFrame containing data.\n",
    "    \n",
    "    Output:\n",
    "    A concatenated DataFrame containing\n",
    "        - the original data\n",
    "        - t-6hrs (1hr avg)\n",
    "        - t-5hrs (1hr avg)\n",
    "        - t-3hrs (30min avg)\n",
    "        - t-1hrs (30min avg)\n",
    "        - t-45min (instant)\n",
    "        - t-30min (instant)\n",
    "        - t-15min (instant)\n",
    "        - t-10min (instant)\n",
    "    '''\n",
    "    return pd.concat((data,\n",
    "                      hist6hr(data),hist5hr(data),\n",
    "                      hist3hr(data),hist1hr(data),\n",
    "                      hist45min(data),hist30min(data),\n",
    "                      hist15min(data),hist10min(data)),axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "ExecuteTime": {
     "end_time": "2019-02-20T16:19:49.104912Z",
     "start_time": "2019-02-20T16:19:48.762819Z"
    }
   },
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.8"
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
