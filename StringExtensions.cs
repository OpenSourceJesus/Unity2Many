public static class StringExtensions
{
	public static string SubstringStartEnd (this string str, int startIndex, int endIndex)
	{
		return str.Substring(startIndex, endIndex - startIndex);
	}

	public static string RemoveStartEnd (this string str, int startIndex, int endIndex)
	{
		return str.Remove(startIndex, endIndex - startIndex);
	}

	public static string GetIntersection (this string str, string str2, int startIndex, int count)
	{
		string output = "";
		for (int i = startIndex; i < startIndex + count; i ++)
		{
			if (str.Length <= i || str2.Length <= i)
				return output;
			char c = str[i];
			if (c == str2[i])
				output += c;
			else if (output != "")
				return output;
		}
		return output;
	}

	public static int IndexOfMatchingRightParenthesis (this string str, int charIndex)
	{
		int parenthesisTier = 1;
		int indexOfParenthesis = charIndex;
		while (indexOfParenthesis != -1)
		{
			indexOfParenthesis = str.IndexOfAny(new char[] { '(', ')' }, indexOfParenthesis + 1);
			if (indexOfParenthesis != -1)
			{
				if (str[indexOfParenthesis] == '(')
					parenthesisTier += 1;
				else
				{
					parenthesisTier -= 1;
					if (parenthesisTier == 0)
						return indexOfParenthesis;
				}
			}
		}
		return -1;
	}

	public static int IndexOfMatchingRightGenericSymbol (this string str, int charIndex)
	{
		int genericTier = 1;
		int indexOfGeneric = charIndex;
		while (indexOfGeneric != -1)
		{
			indexOfGeneric = str.IndexOfAny(new char[] { '<', '>' }, indexOfGeneric + 1);
			if (indexOfGeneric != -1)
			{
				if (str[indexOfGeneric] == '<')
					genericTier += 1;
				else
				{
					genericTier -= 1;
					if (genericTier == 0)
						return indexOfGeneric;
				}
			}
		}
		return -1;
	}

	public static bool IsInString (this string str, int charIndex)
	{
		bool output = false;
		int indexOfDoubleQuote = -1;
		do
		{
			indexOfDoubleQuote = str.IndexOf('\"', indexOfDoubleQuote + 1);
			if (indexOfDoubleQuote > charIndex)
				return output;
			else if (indexOfDoubleQuote != -1)
				output = !output;
		} while (indexOfDoubleQuote != -1);
		return output;
	}

	public static bool IsInGenerics (this string str, int charIndex)
	{
		int indexOfLeftGeneric = str.LastIndexOf('<', charIndex);
		int indexOfRightGeneric = str.IndexOf('>', charIndex);
		return indexOfLeftGeneric < charIndex && indexOfRightGeneric > charIndex && str[charIndex + 1] != '=';
	}

	public static bool IsInChar (this string str, int charIndex)
	{
		return str[charIndex - 1] == '\'' && str[charIndex + 1] == '\'';
	}

	public static bool IsInNumber (this string str, int charIndex)
	{
		int i;
		return (charIndex > 0 && (int.TryParse("" + str[charIndex - 1], out i) || str[charIndex - 1] == '.')) || (charIndex < str.Length - 1 && (int.TryParse("" + str[charIndex + 1], out i) || str[charIndex + 1] == '.'));
	}
}
