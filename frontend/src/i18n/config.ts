import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './locales/en.json';
import hi from './locales/hi.json';

export interface LanguageOption {
  code: string;
  name: string;
  nativeName: string;
  isComplete: boolean;
}

export const SUPPORTED_LANGUAGES: LanguageOption[] = [
  { code: 'en', name: 'English', nativeName: 'English', isComplete: true },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', isComplete: true },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা', isComplete: false },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', isComplete: false },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', isComplete: false },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी', isComplete: false },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી', isComplete: false },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ', isComplete: false },
  { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം', isComplete: false },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', isComplete: false },
];

const savedLanguage = localStorage.getItem('anveksha_lang') || 'en';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      hi: { translation: hi },
      bn: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'সঠিকতার ওপারে।', tagline_part2: 'সমগ্র জনসংখ্যা জুড়ে।' },
          nav: { home: 'হোম', new_test: 'নতুন পরীক্ষা', results: 'ফলাফল', history: 'ইতিহাস', learn: 'শিখুন', settings: 'সেটিংস' }
        }
      },
      ta: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'துல்லியத்திற்கு அப்பால்.', tagline_part2: 'மக்கள் தொகை முழுவதும்.' },
          nav: { home: 'முகப்பு', new_test: 'புதிய சோதனை', results: 'முடிவுகள்', history: 'வரலாறு', learn: 'கற்க', settings: 'அமைப்புகள்' }
        }
      },
      te: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'ఖచ్చితత్వానికి మించి.', tagline_part2: 'జనాభా అంతటా.' },
          nav: { home: 'హోమ్', new_test: 'కొత్త పరీక్ష', results: 'ఫలితాలు', history: 'చరిత్ర', learn: 'నేర్చుకోండి', settings: 'సెట్టింగ్‌లు' }
        }
      },
      mr: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'अचूकतेच्या पलीकडे.', tagline_part2: 'सर्व लोकसंख्येमध्ये.' },
          nav: { home: 'मुख्यपृष्ठ', new_test: 'नवीन चाचणी', results: 'निकाल', history: 'इतिहास', learn: 'शिकणे', settings: 'सेटिंग्ज' }
        }
      },
      gu: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'ચોકસાઈથી આગળ.', tagline_part2: 'સમગ્ર વસ્તીમાં.' },
          nav: { home: 'હોમ', new_test: 'નવી કસોટી', results: 'પરિણામો', history: 'ઇતિહાસ', learn: 'શીખો', settings: 'સેટિંગ્સ' }
        }
      },
      kn: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'ನಿಖರತೆಯನ್ನು ಮೀರಿ.', tagline_part2: 'ಜನಸಂಖ್ಯೆಯಾದ್ಯಂತ.' },
          nav: { home: 'ಮುಖಪುಟ', new_test: 'ಹೊಸ ಪರೀಕ್ಷೆ', results: 'ಫಲಿತಾಂಶಗಳು', history: 'ಇತಿಹಾಸ', learn: 'ಕಲಿಯಿರಿ', settings: 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು' }
        }
      },
      ml: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'കൃത്യതയ്ക്കപ്പുറം.', tagline_part2: 'ജനസംഖ്യയിലുടനീളം.' },
          nav: { home: 'ഹോം', new_test: 'പുതിയ പരിശോധന', results: 'ഫലങ്ങൾ', history: 'ചരിത്രം', learn: 'പഠിക്കുക', settings: 'ക്രമീകരണങ്ങൾ' }
        }
      },
      pa: {
        translation: {
          app: { name: 'ANVEKSHA', tagline_part1: 'ਸ਼ੁੱਧਤਾ ਤੋਂ ਪਰੇ।', tagline_part2: 'ਸਾਰੀ ਆਬਾਦੀ ਵਿੱਚ।' },
          nav: { home: 'ਮੁੱਖ ਪੰਨਾ', new_test: 'ਨਵਾਂ ਟੈਸਟ', results: 'ਨਤੀਜੇ', history: 'ਇਤਿਹਾਸ', learn: 'ਸਿੱਖੋ', settings: 'ਸੈਟਿੰਗਾਂ' }
        }
      }
    },
    lng: savedLanguage,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
