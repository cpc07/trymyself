class CenterIndexFinder:
    @staticmethod
    def find_center_index(nums):
        if not nums:
            return -1

        total_sum = sum(nums)
        left_sum = 0

        for i in range(len(nums)):
            right_sum = total_sum - left_sum - nums[i]
            if left_sum == right_sum:
                return i
            left_sum += nums[i]

        return -1

def main():
    input_nums = input("请输入一个整数数组（例如：[1,7,3,6,5,6]）: ")
    nums = list(map(int, input_nums.strip('[]').replace(' ', '').split(',')))
    result = CenterIndexFinder.find_center_index(nums)
    print(f"中心下标是: {result}")

if __name__ == "__main__":
    main()